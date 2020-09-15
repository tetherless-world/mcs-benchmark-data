<<<<<<< HEAD
# CommonsenseBenchmark

This repo contains a light-weight code template for converting various commonsense question answering benchmarks 
into a general format. The Benckmark base class defines a list of interfaces that should be implemented accordingly 
when converting a specific benchmark. Below are some examples illustrating the defined schema:
```
[
  {
    "benchmarkId": "commonsenseqa",
    "choices": [
      {
        "label": "A",
        "text": "bank"
      },
      {
        "label": "B",
        "text": "library"
      },
      {
        "label": "C",
        "text": "department store"
      },
      {
        "label": "D",
        "text": "mall"
      },
      {
        "label": "E",
        "text": "new york"
      }
    ],
    "id": "1afa02df02c908a558b4036e80242fac",
    "questionSetId": "dev",
    "text": "A revolving door is convenient for two direction travel, but it also serves as a security measure at a what?",
    "questionType": [
      "multiple choice"
    ],
    "sourceConceptnetConcept": "revolving door",
    "correctChoiceLabel": "A"
  },
  {
    "benchmarkId": "cycic",
    "choices": [
      {
        "label": "0",
        "text": "True"
      },
      {
        "label": "1",
        "text": "False"
      }
    ],
    "id": "325861",
    "questionSetId": "training",
    "text": "True or false: When you encounter a cat, you expect to be able to see it's mouth.",
    "questionType": [
      "true/false"
    ],
    "categories": [
      "object properties",
      "animals"
    ],
    "correctChoiceLabel": "0"
  },
  {
    "benchmarkId": "cycic",
    "choices": [
      {
        "label": "0",
        "text": "Sprite"
      },
      {
        "label": "1",
        "text": "root beer"
      },
      {
        "label": "2",
        "text": "strawberry soft drink"
      },
      {
        "label": "3",
        "text": "fox meat"
      },
      {
        "label": "4",
        "text": "newborn vitamin"
      }
    ],
    "id": "214945",
    "questionSetId": "training",
    "text": "It's too bad Bobby served ______. Everybody at the party follows the vegetarian diet program.",
    "questionType": [
      "multiple choice",
      "blanks"
    ],
    "categories": [
      "norms"
    ],
    "correctChoiceLabel": "3",
    "chosenChoiceLabel": "3"
  },
  {
    "benchmarkId": "socialiqa",
    "id": "socialiqa-dev-2",
    "questionSetId": "dev",
    "questionType": "multiple choice",
    "categories": [
      
    ],
    "text": "What will patients want to do next?",
    "context": "Sasha protected the patients' rights by making new laws regarding cancer drug trials.",
    "concept": "",
    "choices": [
      {
        "label": "1",
        "text": "write new laws"
      },
      {
        "label": "2",
        "text": "get petitions signed"
      },
      {
        "label": "3",
        "text": "live longer"
      }
    ],
    "correctChoiceLabel": "2",
    "chosenChoiceLabel": ""
  },
  {
    "benchmarkId": "physicaliqa",
    "id": "c36c629e-12e9-43cc-8936-e1a96d869ab0",
    "questionSetId": "dev",
    "questionType": "multiple choice",
    "categories": [
      
    ],
    "text": "How do I ready a guinea pig cage for it's new occupants?",
    "context": "",
    "concept": "",
    "choices": [
      {
        "label": "0",
        "text": "Provide the guinea pig with a cage full of a few inches of bedding made of ripped paper strips, you will also need to supply it with a water bottle and a food dish."
      },
      {
        "label": "1",
        "text": "Provide the guinea pig with a cage full of a few inches of bedding made of ripped jeans material, you will also need to supply it with a water bottle and a food dish."
      }
    ],
    "correctChoiceLabel": "0",
    "chosenChoiceLabel": ""
  }
]
```
To convert a new benchmark, place its data under a new directory created for it, create a new python class implementing 
the benchmark interfaces. The converted data should be stored under the ./converted dir, categorized by benchmarks.

Benchmarks supported:
## CycIC
## SocialIQA
## PhysicalIQA
=======
# benchmark_etl
>>>>>>> benchmark_etl/master
