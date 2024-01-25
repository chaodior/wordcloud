from flask import Flask, render_template, request, jsonify
import spacy
from wordcloud import WordCloud
import base64
from io import BytesIO

app = Flask(__name__)

# 加载spaCy的英文模型
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud():
    try:
        # 从请求中获取用户输入的文本
        user_text = request.form['text']

        # 处理文本并提取关键词
        doc = nlp(user_text)
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]

        # 生成文字云
        wordcloud = WordCloud(width=800, height=400).generate(" ".join(keywords))

        # 将生成的文字云转化为图像
        image_data = wordcloud.to_image()

        # 将图像数据转化为Base64编码
        image_base64 = base64.b64encode(BytesIO(image_data).read()).decode('utf-8')

        # 返回关键词和文字云图像
        return render_template('result.html', keywords=keywords, wordcloud_image=image_base64)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
