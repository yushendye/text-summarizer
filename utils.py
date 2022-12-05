import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

def read_input_from_text(input_text):
    article = input_text.split('. ')
    sentences = []
    for line in article:
        sentences.append(line.replace('[^a-zA-Z]', '').split(" "))
    sentences.pop()
    
    return sentences

def read_article(input_file):
    file = open(input_file, 'r')
    lines = file.readlines()
    
    article = lines[0].split('. ')
    sentences = []
    for line in article:
        sentences.append(line.replace('[^a-zA-Z]', '').split(" "))
    sentences.pop()
    
    return sentences


def sentence_similarity(sent1, sent2, stop_words = None):
    if stop_words is None:
        stop_words = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = sent1 + sent2

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for word in sent1:
        if word in stop_words:
            continue
        vector1[all_words.index(word)] += 1

    for word in sent2:
        if word in stop_words:
            continue
        vector2[all_words.index(word)] += 1

    return 1 - cosine_distance(vector1, vector2)


def build_similarity_index(sentences, stop_words = None):
    if stop_words is None:
        stop_words = []

    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stop_words)

    return similarity_matrix

def generate_summary(file_name = None, input_text = None, top_n = 5):
    nltk.download('stopwords')
    stop_words = stopwords.words('english')

    summary = []

    if file_name is not None and input_text is None:
        sentences = read_article(file_name)
    if file_name is None and input_text is not None:
        sentences = read_input_from_text(input_text)

    sentences_similarity_matrix = build_similarity_index(sentences, stop_words)

    sentence_similarity_graph = nx.from_numpy_array(sentences_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)

    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    print('Ranked sent : ', ranked_sentences)

    for i in range(top_n):
        summary.append(" ".join(ranked_sentences[i][1]))
    
    return summary


if __name__ == '__main__':
    generate_summary(input_text='In an attempt to build an AI-ready workforce, Microsoft announced Intelligent Cloud Hub which has been launched to empower the next generation of students with AI-ready skills. Envisioned as a three-year collaborative program, Intelligent Cloud Hub will support around 100 institutions with AI infrastructure, course content and curriculum, developer support, development tools and give students access to cloud and AI services. As part of the program, the Redmond giant which wants to expand its reach and is planning to build a strong developer ecosystem in India with the program will set up the core AI infrastructure and IoT Hub for the selected campuses. The company will provide AI development tools and Azure AI services such as Microsoft Cognitive Services, Bot Services and Azure Machine Learning.According to Manish Prakash, Country General Manager-PS, Health and Education, Microsoft India, said, "With AI being the defining technology of our time, it is transforming lives and industry and the jobs of tomorrow will require a different skillset. This will require more collaborations and training and working with AI. That’s why it has become more critical than ever for educational institutions to integrate new cloud and AI technologies. The program is an attempt to ramp up the institutional set-up and build capabilities among the educators to educate the workforce of tomorrow." The program aims to build up the cognitive skills and in-depth understanding of developing intelligent cloud connected solutions for applications across industry. Earlier in April this year, the company announced Microsoft Professional Program In AI as a learning track open to the public. The program was developed to provide job ready skills to programmers who wanted to hone their skills in AI and data science with a series of online courses which featured hands-on labs and expert instructors as well. This program also included developer-focused AI school that provided a bunch of assets to help build AI skills.', top_n = 2)