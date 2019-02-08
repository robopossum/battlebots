#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 23:02:45 2019

@author: tom
"""

import numpy as np
import gym
from customAIGYM import customAIGYM
from keras.models import Sequential
from keras.layers import Dense, Reshape, Activation, Flatten, LSTM
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory




# Get the environment and extract the number of actions.
from customAIGYM import firstAttempt

env = firstAttempt.FooEnv()
np.random.seed(123)

nb_actions = 7

# Next, we build a very simple model.
model = Sequential()

model.add(Dense(47, input_shape=(47, )))
#model.add(ReShape())
model.add(Activation('relu'))
#model.add(Flatten(input_shape=(1,) + (47,), batch_input_shape=((47,1, 24))))
# model.add(LSTM(360, recurrent_activation='hard_sigmoid', use_bias=True,
#                 kernel_initializer='glorot_uniform',
#                 recurrent_initializer='orthogonal', bias_initializer='zeros',
#                 unit_forget_bias=True, kernel_regularizer=None,
#                 recurrent_regularizer=None, bias_regularizer=None,
#                 activity_regularizer=None, kernel_constraint=None,
#                 recurrent_constraint=None, bias_constraint=None,
#                 dropout=0.0, recurrent_dropout=0.0, implementation=1,
#                 return_sequences=True, return_state=False, go_backwards=False,
#                 stateful=True, unroll=False))

model.add(Dense(225))
#model.add(Activation('sigmoid'))
model.add(Dense(250))
#model.add(Activation('sigmoid'))
model.add(Dense(250))
model.add(Activation('sigmoid'))
# model.add(LSTM(360, recurrent_activation='hard_sigmoid', use_bias=True,
#                kernel_initializer='glorot_uniform',
#                recurrent_initializer='orthogonal', bias_initializer='zeros',
#                unit_forget_bias=True, kernel_regularizer=None,
#                recurrent_regularizer=None, bias_regularizer=None,
#                activity_regularizer=None, kernel_constraint=None,
#                recurrent_constraint=None, bias_constraint=None,
#                dropout=0.0, recurrent_dropout=0.0, implementation=1,
#                return_sequences=True, return_state=False, go_backwards=False,
#                stateful=True, unroll=False, input_shape=(360, 1)))
# model.add(Activation('sigmoid'))
model.add(Dense(112))
model.add(Activation('sigmoid'))
#model.add(Reshape((5600, )))
model.add(Dense(nb_actions))
model.add(Activation('sigmoid'))
print(model.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=50)
policy = BoltzmannQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions,
               enable_double_dqn=True, memory=memory, nb_steps_warmup=128,
               target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
dqn.fit(env, nb_steps=50000, visualize=False, verbose=2)


# After training is done, we save the final weights.
dqn.save_weights('dqn_{}_weights.h5f'.format("babyStepsFirstQN"), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=1, visualize=True)




from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model





main_input = Input(shape=(100,), dtype='int32', name='main_input')

# This embedding layer will encode the input sequence
# into a sequence of dense 512-dimensional vectors.
x = Embedding(output_dim=512, input_dim=10000, input_length=100)(main_input)

# A LSTM will transform the vector sequence into a single vector,
# containing information about the entire sequence
lstm_out = LSTM(32)(x)

auxiliary_output = Dense(1, activation='sigmoid', name='aux_output')(lstm_out)

auxiliary_input = Input(shape=(5,), name='aux_input')
x = keras.layers.concatenate([lstm_out, auxiliary_input])

# We stack a deep densely-connected network on top
x = Dense(64, activation='relu')(x)
x = Dense(64, activation='relu')(x)
x = Dense(64, activation='relu')(x)

# And finally we add the main logistic regression layer
main_output = Dense(1, activation='sigmoid', name='main_output')(x)
model = Model(inputs=[main_input, auxiliary_input], outputs=[main_output, auxiliary_output])

model.compile(optimizer='rmsprop', loss='binary_crossentropy',
              loss_weights=[1., 0.2])



model.fit([headline_data, additional_data], [labels, labels],
          epochs=50, batch_size=32)

