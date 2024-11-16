# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from rasa_sdk import Action


class ActionDoSomething(Action):
  def name(self):
    return "action_do_something"

  def run(self, dispatcher, tracker, domain):
    text = "um simples texto"
    dispatcher.utter_message(text=text)
    return []
  
