from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = 'your-api-key-here'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code_snippet = request.form['code']
        ai_review = review_code(code_snippet)
        return render_template('index.html', original_code=code_snippet, ai_review=ai_review)
    return render_template('index.html', original_code='', ai_review='')


def review_code(code_snippet):
    try:
        response = openai.Completion.create(
            engine="code-davinci-002",  # You can choose a different model based on your requirement
            prompt=f"Review the following code snippet:\n\n{code_snippet}\n\n",
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
