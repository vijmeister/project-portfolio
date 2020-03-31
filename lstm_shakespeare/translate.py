from __future__ import unicode_literals, print_function, division
from io import open
import unicodedata
import string
import re
import random

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
import nltk
from nltk.corpus import wordnet

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

SOS_token = 0
EOS_token = 1


class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s

class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size, num_layers = 2)

    def forward(self, input, hidden):
        embedded = self.embedding(input).view(1, 1, -1)
        output = embedded
        output, hidden = self.gru(output, hidden)
        return output, hidden

    def initHidden(self):
        return torch.zeros(2, 1, self.hidden_size, device=device)

class DecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size):
        super(DecoderRNN, self).__init__()
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(output_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size, num_layers = 2)
        self.out = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        output = self.embedding(input).view(1, 1, -1)
        output = F.relu(output)
        output, hidden = self.gru(output, hidden)
        output = self.softmax(self.out(output[0]))
        return output, hidden

    def initHidden(self):
        return torch.zeros(2, 1, self.hidden_size, device=device)

MAX_LENGTH = 50

class AttnDecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size, dropout_p=0.1, max_length=MAX_LENGTH):
        super(AttnDecoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.dropout_p = dropout_p
        self.max_length = max_length

        self.embedding = nn.Embedding(self.output_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.gru = nn.GRU(self.hidden_size, self.hidden_size, num_layers = 2)
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input, hidden, encoder_outputs):
        embedded = self.embedding(input).view(1, 1, -1)
        embedded = self.dropout(embedded)

        attn_weights = F.softmax(
            self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
        attn_applied = torch.bmm(attn_weights.unsqueeze(0),
                                 encoder_outputs.unsqueeze(0))

        output = torch.cat((embedded[0], attn_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)

        output = F.relu(output)
        output, hidden = self.gru(output, hidden)

        output = F.log_softmax(self.out(output[0]), dim=1)
        return output, hidden, attn_weights

    def initHidden(self):
        return torch.zeros(2, 1, self.hidden_size, device=device)

def indexesFromSentence(lang, sentence):
    #print(lang.word2index)
    for_tensor = []
    proper_nouns = []
    tokens = nltk.word_tokenize(sentence)
    pos_tag = nltk.pos_tag(tokens)
    ptd = dict()
    for pt in pos_tag:
        if pt[0] not in ptd:
            ptd[pt[0]] = pt[1]

    for word in sentence.split(' '):
        if word in lang.word2index:
            for_tensor.append(lang.word2index[word])
        else: 
            for_tensor.append(lang.word2index['oberon'])
            """if ptd[word] == 'NNP':
                for_tensor.append(lang.word2index['Oberon'])
            elif(ptd[word] == 'NN'):
                #for_tensor.append(lang.word2index['king'])
                synonyms = [] 
  
                for syn in wordnet.synsets(word): 
                    for l in syn.lemmas(): 
                        synonyms.append(l.name()) 
            
                for synonym in synonyms:
                    if synonym in lang.word2index:
                        for_tensor.append(lang.word2index[synonym])
                        print("match: " + synonym)
                        break
                    else:
                        print(synonym)"""

            #print(set(synonyms))
            proper_nouns.append((word,ptd[word]))
    
    return (for_tensor,proper_nouns)

def tensorFromSentence(lang, sentence):
    indexes = indexesFromSentence(lang, sentence)[0]
    print(indexesFromSentence(lang, sentence)[1])
    indexes.append(EOS_token)
    return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1),indexesFromSentence(lang, sentence)[0]


def tensorsFromPair(pair):
    input_tensor = tensorFromSentence(input_lang, pair[0])[0]
    target_tensor = tensorFromSentence(output_lang, pair[1])[0]
    return (input_tensor, target_tensor)

teacher_forcing_ratio = 0.5

def evaluate(encoder, decoder, sentence, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_tensor = tensorFromSentence(input_lang, sentence)[0]
        proper_nouns = tensorFromSentence(input_lang, sentence)[1]
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS

        decoder_hidden = encoder_hidden

        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(output_lang.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()
        
        #ind = 0
        for word in decoded_words:
            
            if word.lower() == 'oberon':
                word = proper_nouns[::-1].pop()
        return decoded_words, decoder_attentions[:di + 1]

"""def splice_output(proper_nouns, decoded_words, input_string, lang):
    pass
    return"""

import pickle

pickle_off0 = open("il.pickle","rb")
input_lang = pickle.load(pickle_off0)
#print(input_lang.word2index)

pickle_offz = open("ol.pickle","rb")
output_lang = pickle.load(pickle_offz)
#print(output_lang.word2index)

pickle_off = open("enc.pickle","rb")
enc = pickle.load(pickle_off)

pickle_off1 = open("dec.pickle","rb")
dec = pickle.load(pickle_off1)

MAX_LENGTH = 50

with open('test.txt', 'rb') as f:
    text = f.read().decode('utf8')

print(text)

text = unicodeToAscii(text)

print(text)

#tokens = nltk.word_tokenize(text)

#print(nltk.pos_tag(tokens))

text = normalizeString(text)

print(text)

print(evaluate(enc, dec, text)[0])

"""for line in text:
    #print(line)
    print(evaluate(enc, dec, line))"""
