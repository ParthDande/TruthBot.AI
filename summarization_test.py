from flask import Flask, request, render_template, jsonify
import requests


import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
result = query({
	"inputs":"""
Israel also bombed targets in the northeastern Baalbek and Hermel regions, where a shepherd was killed and two family members were wounded, according to the news agency. It said a total of 30 people were wounded in strikes. The Lebanese Health Ministry asked hospitals in southern Lebanon and the eastern Bekaa valley to postpone surgeries that could be done later. The ministry said in a statement that its request aimed to keep hospitals ready to deal with people wounded by “Israel’s expanding aggression on Lebanon.” 
 The official, speaking on condition of anonymity in keeping with regulations, said the strikes are aimed at curbing Hezbollah's ability to launch more strikes into Israel. Lebanese media reported that residents received text messages urging them to move away from any building where Hezbollah stores arms until further notice.
 killing some 1,200 people, mostly civilians, and abducting around 250. Some 100 captives are still held in Gaza, a third of whom are believed to be dead, after most of the rest were released during a weeklong cease-fire in November. Israel's offensive has killed over 41,000 Palestinians, according to Gaza's Health Ministry, which does not differentiate between civilians and fighters in its count. It says women and children make up a little over half of those killed. Israel says it has killed over 17,000 militants, without providing evidence
""","max_length": 150, "min_length": 50})
print(result[0]['summary_text'])