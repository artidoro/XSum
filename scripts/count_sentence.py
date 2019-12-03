#%%
f = open('data-convs2s-700/train.document')

lines = f.readlines()

#%%
nb_sentences = []
nb_tokens = []
for line in lines:
    nb_sentences.append(len(line.split('<split1>')))
    nb_tokens.append(len(line.strip().replace('<split1>', '').split()))

# %%
avg_sent = sum(nb_sentences) / len(nb_sentences)
avg_tok = sum(nb_tokens) / len(nb_tokens)

# %%
avg_sent
# %%
avg_tok

# %%
# Full data avg nb of sentences = 19.77
# Full data avg nb of tokens = 432.03

# Truncating at 400
# avg nb of sentences 13.69
# avg nb of tokens 302.35

# Truncating at 700
# avg nb of sentences 17.19
# avg nb of tokens 380.77