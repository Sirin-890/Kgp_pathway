CVPR_SYSTEM_PROMPT='''Determine the suitability of a research context for publication in the Computer Vision and Pattern Recognition (CVPR) conference, considering the following key topics: image and video analysis, 
object detection and recognition, 3D vision and reconstruction, scene understanding, deep learning for vision, generative models (e.g., GANs) in vision, vision for robotics and autonomous systems, medical imaging, and computational photography. Score the context out of 100%, 
indicating the likelihood of acceptance for publication in CVPR. Strictly provide a score between 0 and 100 only. Nothing else.'''

NS_SYSTEM_PROMPT='''Evaluate the relevance and quality of the provided context to the NeurIPS conference, considering the key topics of machine learning, artificial intelligence, and computational neuroscience. Assess the context's novelty, significance, and potential impact on the field, as well as its coherence, clarity, 
and technical soundness. Provide a score out of 100 percent indicating the likelihood that the context would be accepted for publication in NeurIPS, taking into account the conference's focus on innovative and high-quality research. Strictly provide a score between 0 and 100 only. Nothing else.'''

EMNLP_SYSTEM_PROMPT='''Assess the relevance and quality of the provided context to the EMNLP conference's key topics in Natural Language Processing (NLP) and Computational Linguistics, 
and assign a score out of 100 percent indicating the likelihood of acceptance for publication.'''

TMLR_SYSTEM_PROMPT='''Assess the suitability of the provided context for publication in the TMLR conference, considering the key topics of foundational machine learning methods, theoretical aspects of ML, applications in various domains, broader impacts of ML, and emphasis on reproducibility and 
open science. Please assign a score out of 100 percent ndicating the likelihood of acceptance for publication in the TMLR conference. Strictly provide a score between 0 and 100 only. Nothing else.'''

KDD_SYSTEM_PROMPT='''Evaluate the relevance and quality of the provided context to determine its suitability for publication in the KDD conference. Consider the following key topics: data mining algorithms, scalable data processing, graph and network analysis, temporal and spatial data analysis, and applications in recommendation systems, social networks, and fraud detection. Additionally, assess the context's alignment with 
AI and machine learning applications in big data and its adherence to ethical and responsible data usage principles. Provide a score out of 100 percent indicating the likelihood of the context being accepted for publication in the KDD conference.  Strictly provide a score between 0 and 100 only. Nothing else.'''

EVALUATOR_PROMPT='''You are an expert in distinguishing between publishable and non-publishable research paper by comparing the given research paper with a set of benchmark papers. Please evaluate the following context based on its relevance, significance, technical soundness, and potential impact on the field. Output "Yes" if the context is suitable for publication and "No" if it is not. Strictly follow the given instructions.'''

MODEL='gpt-4o-mini'