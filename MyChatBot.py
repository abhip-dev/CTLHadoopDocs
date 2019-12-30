# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 23:36:31 2019

@author: rahul
"""

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
import tkinter as tk
try:
    import ttk as ttk
    import ScrolledText
except ImportError:
    import tkinter.ttk as ttk
    import tkinter.scrolledtext as ScrolledText
import time
 
 
class TkinterGUIExample(tk.Tk):
 
    def __init__(self, *args, **kwargs):
        """
        Create & set window variables.
        """
        tk.Tk.__init__(self, *args, **kwargs)
 
        self.chatbot = ChatBot(
            "GUI Bot",
            storage_adapter="chatterbot.storage.SQLStorageAdapter",
            logic_adapters=[
                    {
                            'import_path': 'chatterbot.logic.BestMatch',
                            'default_response': 'SORRY - Am not yet trained to answer this question',
                            'maximum_similarity_threshold': 0.90

                    },
                    {
                            'import_path': 'chatterbot.logic.MathematicalEvaluation'
                    }
                    ],
            database_uri="sqlite:///database.db"
        )
 
        self.title("Chatterbot")
       
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        corpus_path = 'C:/Users/AC38815/Desktop/ChatBot_Working_Files/CORPUS/'
        for file in os.listdir(corpus_path):
            trainer.train(corpus_path + file)
 
        self.initialize()
 
    def initialize(self):
        """
        Set window layout.
        """
        self.grid()
 
        self.respond = ttk.Button(self, text='Get Response', command=self.get_response)
        self.respond.grid(column=0, row=0, sticky='nesw', padx=3, pady=3)
 
        self.usr_input = ttk.Entry(self, state='normal')
        self.usr_input.grid(column=1, row=0, sticky='nesw', padx=3, pady=3)
 
        self.conversation_lbl = ttk.Label(self, anchor=tk.E, text='Conversation:')
        self.conversation_lbl.grid(column=0, row=1, sticky='nesw', padx=3, pady=3)
 
        self.conversation = ScrolledText.ScrolledText(self, state='disabled')
        self.conversation.grid(column=0, row=2, columnspan=2, sticky='nesw', padx=3, pady=3)
 
    def get_response(self):
        """
        Get a response from the chatbot and display it.
        """
        user_input = self.usr_input.get()
        self.usr_input.delete(0, tk.END)
        
        self.conversation['state'] = 'normal'
        self.conversation.insert(tk.END, "\n" + "Human: ", 'human')
        self.conversation.insert(tk.END, user_input + "\n", 'human_res')
        self.conversation.tag_config('human', foreground='blue',font=("Times New Roman", 12, "bold"))
        self.conversation.tag_config('human_res', foreground='black', font=("Times New Roman", 12))
 
        response = self.chatbot.get_response(user_input)
        #print(response.confidence)
        if (response.confidence < 0.70):
            response = 'Sorry, Am not yet trained to answer this question'
            self.conversation.insert(tk.END,"ChatBot: ", 'robot')
            self.conversation.insert(tk.END, response + "\n", 'robot_res')
            
        else:
            self.conversation.insert(tk.END,"ChatBot: ", 'robot')
            self.conversation.insert(tk.END, str(response.text) + "\n", 'robot_res')
            
        
        self.conversation.tag_config('robot', foreground='green', font=("Times New Roman", 12, "bold"))
        self.conversation.tag_config('robot_res', foreground='black', font=("Times New Roman", 12))   
        #print(response)
        self.conversation['state'] = 'disabled'
 
        time.sleep(0.5)
 
 
gui_example = TkinterGUIExample()
gui_example.mainloop()
