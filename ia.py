import spacy
from spacy.tokens import Span,DocBin
nlp = spacy.blank("es")

doc1 = nlp("Rusia a Ucrania y ahora los imbéciles venecos a Colombia.  jajajajajajaja")
doc1.ents = [Span(doc1, 7, 8, label="INSULTO"), Span(doc1, 6, 7, label="INSULTO")]

doc2 = nlp("Cuando SleepyJoe nos libere de los venecos hincha bolas")
doc2.ents = [Span(doc2, 6, 9, label="INSULTO")]

doc = nlp("Francia en la W “yo no vine por un cargo, vine por una transformación… que vivir en Colombia sea una alegría” Sin egos, eso es el pacto. Francia Marquez dando clases de altura.")

doc4 = nlp("venecos hijos de puta")
doc4.ents = [Span(doc4, 0, 1, label="INSULTO"), Span(doc4, 1, 4, label="INSULTO") ]

doc3 = nlp("Mientras los venezolanos se mueren de hambre, sus dirigentes son multimillonarios.")

doc5 = nlp("Un millón de personas huyendo de Ucrania,  nadie habla ahora de los 6 millones de Venezolanos, que huyeron del Dictador Maduro")

doc6 = nlp("marika el veneco es un ladron")
doc6.ents = [Span(doc6, 0, 1, label="INSULTO"),Span(doc6, 2, 3, label="INSULTO"),Span(doc6, 5, 6, label="INSULTO")]

doc7 = nlp("Ahora algunos dicen que los votos de Francia Márquez no son de ella, que es una estrategia de otros, misoginia y racismo en un solo paquetico.")

docs = [doc7,doc1,doc2,doc3,doc,doc4,doc5]

train_docs = docs[:len(docs) // 2]
dev_docs = docs[len(docs) // 2:]

train_docbin = DocBin(docs=train_docs)
train_docbin.to_disk("./train.spacy")
dev_docbin = DocBin(docs=dev_docs)
dev_docbin.to_disk("./dev.spacy")