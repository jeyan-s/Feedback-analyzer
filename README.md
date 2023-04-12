# Feedback Review World

# Live Demo
https://jeyan-s-feedback-analyzer-home-uql886.streamlit.app/
# Why Feedback ?
Sharing information on what can be improved helps optimize the work process and get things done in less time.

Using FR World website, employees can provide feedback about their company. Only admin of the application can view the employee name from database others can see only the company name and the feedback.
# Why review ? 
Reviews provide insight into many areas, from culture of organization to competence in specific area.

Organization can review feedbacks provided by employee segregated as positive, negative and neutral feedbacks which are classified by emotional trait and sentimental  analysis of NLP API. They can also improve the company by working on negative feedbacks.

Anyone who want to know more about the company from working employees can view the reviews.
# Usage :
expert.ai NLP API (Emotional traits, Sentiment analysis, Hate speech detection)
# For checking if feedback contains hate speech
```
h_output = client.detection(body={"document": {"text": feedback[0]}}, params={'detector': 'hate-speech', 'language': 'en'})
l = (len(h_output.categories) == 0)
```
# For finding emotions
```
output = client.classification(body={"document": {"text": text}}, params={'taxonomy':'emotional-traits','language':'en'})

```
# For finding sentiment of emotions
```
for category in output.categories:
  op = client.specific_resource_analysis(body={"document": {"text": category.label}},params={'language': 'en', 'resource': 'sentiment'})
```
# Classification based on sentiment score
```
senti = op.sentiment.overall
if(senti < 0):
  dicti["Negative"].append(feedback[0])
  neg += 1
elif(senti == 0):
  dicti["Neutral"].append(feedback[0])
  neu += 1
else:
  dicti["Positive"].append(feedback[0])
  pos += 1
                        
