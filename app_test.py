import uuid
import threading
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from analisar_grafo import analisar_grafo
import json
from analisar_grafo_semantica_heatmap import processar_grafos_e_gerar_saida, heatmap_similaridade_grafos, generate_node_list_json
from ollama_model_manager import OllamaModelManager

app = Flask(__name__)
CORS(app)
tasks = {}
comparisons = {}
IMAGE_DIR = "/home/tiagoriosrocha/Documents/cognee/backend-flask-morehopqa"

#######################################################################################################
#######################################################################################################
#######################################################################################################
FIXED_RESULT1 = {
    "final_answer": "The director of the 2004 film 'The Prince and Me' is Martha Coolidge. The first name 'Martha' has five letters in total, with three letters between the first ('M') and last letter ('a').",
    "nodes": 
    {
        "1840d0e8-63ef-56a5-ab57-974d1557da19": {
            "belongs_to_set": False,
            "created_at": 1759845009264,
            "description": "The Danish monarch who is unexpectedly saved from death, leading to a series of events with Anne Sofie Henning.",
            "id": "1840d0e8-63ef-56a5-ab57-974d1557da19",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "king frederik of denmark",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759845009264,
            "version": 1
        },
        "1c877e38-afdb-5af9-bfa1-c14235256bbe": {
            "belongs_to_set": False,
            "created_at": 1759846558810,
            "description": "A director of films including 'Real Life' and 'Rambling Rose.'",
            "id": "1c877e38-afdb-5af9-bfa1-c14235256bbe",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "martha coolidge",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759846558810,
            "version": 1
        },
        "2c0ab9d2-2991-5742-b083-4747f1c55110": {
            "belongs_to_set": False,
            "created_at": 1759846059491,
            "external_metadata": "{}",
            "id": "2c0ab9d2-2991-5742-b083-4747f1c55110",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_a1a220f8f21dbd8094bc6dbd0e7f22c8",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_a1a220f8f21dbd8094bc6dbd0e7f22c8.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759846059491,
            "version": 1
        },
        "2d894c54-6215-58c2-878b-5258ae2a688a": {
            "belongs_to_set": False,
            "created_at": 1759846718589,
            "id": "2d894c54-6215-58c2-878b-5258ae2a688a",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Section discussing number 4.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759846718589,
            "version": 1
        },
        "2faae991-8084-59f4-becd-e6417659176a": {
            "belongs_to_set": False,
            "created_at": 1759846610669,
            "external_metadata": "{}",
            "id": "2faae991-8084-59f4-becd-e6417659176a",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_a87ff679a2f3e71d9181a67b7542122c",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_a87ff679a2f3e71d9181a67b7542122c.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759846610669,
            "version": 1
        },
        "30ca42a3-ec5a-59d3-9228-0da4f454be03": {
            "belongs_to_set": False,
            "created_at": 1759845853199,
            "external_metadata": "{}",
            "id": "30ca42a3-ec5a-59d3-9228-0da4f454be03",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_986e4ef18b400a6074fc04116fc4f4bd",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_986e4ef18b400a6074fc04116fc4f4bd.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759845853199,
            "version": 1
        },
        "36bbddca-8ba0-5775-835e-3def224b6b8e": {
            "belongs_to_set": False,
            "created_at": 1759846479487,
            "id": "36bbddca-8ba0-5775-835e-3def224b6b8e",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Martha Coolidge is a distinguished filmmaker known for her work as both an actress and director. With notable films like 'Valentino' and 'Rambling Rose,' she made history with the latter being the first film directed by a woman to receive a U.S. release.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759846479487,
            "version": 1
        },
        "3799a3e5-bbf2-560a-86ac-d306bff33be9": {
            "belongs_to_set": False,
            "created_at": 1759846689495,
            "description": "A series of four groundbreaking papers published by Einstein in 1905, contributing significantly to theoretical physics.",
            "id": "3799a3e5-bbf2-560a-86ac-d306bff33be9",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "annus mirabilis papers",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759846689495,
            "version": 1
        },
        "3883cc14-afe1-574b-9cae-3925628fb5da": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 41,
            "created_at": 1759845551444,
            "cut_type": "sentence_end",
            "id": "3883cc14-afe1-574b-9cae-3925628fb5da",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Kam Heskin (born Kam Erika Heskin on May 8, 1973) is an American actress.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759845551444,
            "version": 1
        },
        "39c2c48c-c248-5c33-a4d2-c93b3d4f4405": {
            "belongs_to_set": False,
            "created_at": 1759846367653,
            "external_metadata": "{}",
            "id": "39c2c48c-c248-5c33-a4d2-c93b3d4f4405",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_e2ac58d8ccd36d90a192d6e7ca162a44",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_e2ac58d8ccd36d90a192d6e7ca162a44.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759846367653,
            "version": 1
        },
        "3adcf22e-4932-59a0-899e-1b281fa4112b": {
            "belongs_to_set": False,
            "created_at": 1759846232629,
            "external_metadata": "{}",
            "id": "3adcf22e-4932-59a0-899e-1b281fa4112b",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_50540eb05e14b27c751b5c2bcb248338",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_50540eb05e14b27c751b5c2bcb248338.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759846232629,
            "version": 1
        },
        "3b66f5d8-8c09-5992-a61f-dbcb5e5e4535": {
            "belongs_to_set": False,
            "created_at": 1759845644963,
            "id": "3b66f5d8-8c09-5992-a61f-dbcb5e5e4535",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Overview of Kam Heskin's career",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759845644963,
            "version": 1
        },
        "3d18f258-7e29-50c1-b3dc-4874c7ee86fa": {
            "belongs_to_set": False,
            "created_at": 1759846689495,
            "description": "work",
            "id": "3d18f258-7e29-50c1-b3dc-4874c7ee86fa",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "work",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759846689495,
            "version": 1
        },
        "3fde779e-ee6d-5470-9839-3752302cbca4": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 56,
            "contains": [],
            "created_at": 1759845309859,
            "cut_type": "sentence_end",
            "id": "3fde779e-ee6d-5470-9839-3752302cbca4",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": " The film focuses on Paige Morgan, a pre-med college student in Wisconsin, who is pursued by a prince posing as a normal college student.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759845309859,
            "version": 1
        },
        "485c3abe-cbe6-53c6-8b46-d9e475d02493": {
            "belongs_to_set": False,
            "created_at": 1759845987839,
            "description": "A series of films in which Heskin played the character Paige Morgan from 2006 to 2010.",
            "id": "485c3abe-cbe6-53c6-8b46-d9e475d02493",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "the prince and me film franchise",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759845987839,
            "version": 1
        },
        "531b59b2-3eff-5061-8537-efe0f3921d44": {
            "belongs_to_set": False,
            "created_at": 1759846499234,
            "external_metadata": "{}",
            "id": "531b59b2-3eff-5061-8537-efe0f3921d44",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_0ba6a84a46eabd72876678e70fc132b7",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_0ba6a84a46eabd72876678e70fc132b7.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759846499234,
            "version": 1
        },
        "5811d8f7-e0a7-555f-9066-b81c0f6c9ad0": {
            "belongs_to_set": False,
            "created_at": 1759845656490,
            "external_metadata": "{}",
            "id": "5811d8f7-e0a7-555f-9066-b81c0f6c9ad0",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_01a827d5156ebe7bf6384321dae464f9",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_01a827d5156ebe7bf6384321dae464f9.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759845656490,
            "version": 1
        },
        "66127932-b89f-5cac-bfb3-8132b4119cbd": {
            "belongs_to_set": False,
            "created_at": 1759845987839,
            "description": "A character portrayed by Heskin in The Prince and Me film franchise (2006–2010).",
            "id": "66127932-b89f-5cac-bfb3-8132b4119cbd",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "paige morgan",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759845987839,
            "version": 1
        },
        "66a4cf94-2589-5171-b6e9-82702cc1eaf8": {
            "belongs_to_set": False,
            "created_at": 1759846598071,
            "id": "66a4cf94-2589-5171-b6e9-82702cc1eaf8",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Martha Coolidge was born as Martha Lavey. Between the first letter 'M' and the last letter 'a' of her first name, there are four letters: a-r-t-h.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759846598071,
            "version": 1
        },
        "684c67fa-ef22-5a85-aa3a-ae377468c50a": {
            "belongs_to_set": False,
            "created_at": 1759845072817,
            "external_metadata": "{}",
            "id": "684c67fa-ef22-5a85-aa3a-ae377468c50a",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_0d8bce0ea5edd9bf132de26723b43b94",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_0d8bce0ea5edd9bf132de26723b43b94.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759845072817,
            "version": 1
        },
        "688654a6-42be-5e71-b426-6231f483da19": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 101,
            "contains": [],
            "created_at": 1759845657677,
            "cut_type": "sentence_end",
            "id": "688654a6-42be-5e71-b426-6231f483da19",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": " She began her career playing Caitlin Richards Deschanel on the NBC daytime soap opera \"Sunset Beach\" (1998–1999), before appearing in films \"Planet of the Apes\" (2001 and \"Catch Me If You Can\" (2002).",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759845657677,
            "version": 1
        },
        "6905fcf3-7497-510a-95b0-c26368ec4a3e": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 5,
            "created_at": 1759845438009,
            "cut_type": "sentence_cut",
            "id": "6905fcf3-7497-510a-95b0-c26368ec4a3e",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Kam Heskin",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759845438009,
            "version": 1
        },
        "6a15b02f-0712-56dc-a290-915475d29abb": {
            "belongs_to_set": False,
            "created_at": 1759845009264,
            "description": "A dentist who becomes an assistant royal physician by accident.",
            "id": "6a15b02f-0712-56dc-a290-915475d29abb",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "anne sofie henning",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759845009264,
            "version": 1
        },
        "703f131a-8a0d-5747-803f-9294267118f6": {
            "belongs_to_set": False,
            "created_at": 1759845436848,
            "external_metadata": "{}",
            "id": "703f131a-8a0d-5747-803f-9294267118f6",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_c848f59aad5b304add1773efba5b0762",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_c848f59aad5b304add1773efba5b0762.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759845436848,
            "version": 1
        },
        "7869eb3c-9c39-5f17-ac04-61fb5ab1076d": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 2,
            "created_at": 1759846611790,
            "cut_type": "default",
            "id": "7869eb3c-9c39-5f17-ac04-61fb5ab1076d",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "4",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759846611790,
            "version": 1
        },
        "7ea1b82c-cbfd-52d2-8058-ba9ca0aca9d0": {
            "belongs_to_set": False,
            "created_at": 1759845009264,
            "description": "King Frederik's son and future king.",
            "id": "7ea1b82c-cbfd-52d2-8058-ba9ca0aca9d0",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "prince henrik of denmark",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759845009264,
            "version": 1
        },
        "818506fc-19bc-5fc0-8f96-f0a564a54ff4": {
            "belongs_to_set": False,
            "created_at": 1759846689494,
            "description": "Theoretical physicist known for developing the theory of relativity.",
            "id": "818506fc-19bc-5fc0-8f96-f0a564a54ff4",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "albert einstein",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759846689494,
            "version": 1
        },
        "8598f90c-7a18-5742-85f6-3fd9a634a6d9": {
            "belongs_to_set": False,
            "created_at": 1759846354537,
            "id": "8598f90c-7a18-5742-85f6-3fd9a634a6d9",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "The Prince and Me is directed by Clare Kilner.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759846354537,
            "version": 1
        },
        "87b90780-ba84-50e2-a755-23e6d86cfe4c": {
            "belongs_to_set": False,
            "created_at": 1759846313687,
            "description": "A romantic comedy film released in 2004.",
            "id": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "the prince and me",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759846313687,
            "version": 1
        },
        "9ade0e79-6d39-530e-baeb-1d1b3048bffe": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 7,
            "created_at": 1759844907957,
            "cut_type": "sentence_cut",
            "id": "9ade0e79-6d39-530e-baeb-1d1b3048bffe",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "The Prince and Me",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759844907957,
            "version": 1
        },
        "a1b1f51e-1bd3-551b-bd4a-fe311a7f9b22": {
            "belongs_to_set": False,
            "created_at": 1759844907455,
            "external_metadata": "{}",
            "id": "a1b1f51e-1bd3-551b-bd4a-fe311a7f9b22",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_253becda393cc4221094e8eb3cabf879",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_253becda393cc4221094e8eb3cabf879.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759844907455,
            "version": 1
        },
        "a4596b20-7262-5555-b44b-52c3438ee8da": {
            "belongs_to_set": False,
            "created_at": 1759845425056,
            "id": "a4596b20-7262-5555-b44b-52c3438ee8da",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "A film about Paige Morgan, a pre-med student in Wisconsin, who is courted by a prince pretending to be an ordinary college student.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759845425056,
            "version": 1
        },
        "adba7583-35a0-5239-b4e4-4d34987afcd0": {
            "belongs_to_set": False,
            "created_at": 1759846041678,
            "id": "adba7583-35a0-5239-b4e4-4d34987afcd0",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Heather Graham starred as Elizabeth Bennet in a 2003 independent film adaptation of 'Pride & Prejudice' and played Paige Morgan in 'The Prince and Me' series between 2006-2010.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759846041678,
            "version": 1
        },
        "ae518edb-8a59-5df3-9110-2aaf587e57c8": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 37,
            "created_at": 1759846500364,
            "cut_type": "sentence_end",
            "id": "ae518edb-8a59-5df3-9110-2aaf587e57c8",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "How many letters are there between the first and last letters of the first name of Martha Coolidge?",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759846500364,
            "version": 1
        },
        "ae78912d-86ba-546c-a560-1074c1f53797": {
            "belongs_to_set": False,
            "created_at": 1759845308698,
            "external_metadata": "{}",
            "id": "ae78912d-86ba-546c-a560-1074c1f53797",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_be7a9849b7da3fe3ac22de8ce398250d",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_be7a9849b7da3fe3ac22de8ce398250d.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759845308698,
            "version": 1
        },
        "b234338e-a3a0-590e-ba4c-26f363e04f9e": {
            "belongs_to_set": False,
            "created_at": 1759845840093,
            "id": "b234338e-a3a0-590e-ba4c-26f363e04f9e",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Actress transitioned from daytime soap opera 'Sunset Beach' (1998–1999) to films including 'Planet of the Apes' (2001) and 'Catch Me If You Can' (2002).",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759845840093,
            "version": 1
        },
        "b630e5b0-ae6d-55d0-99fd-039d9e9b5e2b": {
            "belongs_to_set": False,
            "created_at": 1759845987839,
            "description": "film franchise",
            "id": "b630e5b0-ae6d-55d0-99fd-039d9e9b5e2b",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "film franchise",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759845987839,
            "version": 1
        },
        "b838d27b-cd5b-5647-8145-dcdffd120cb5": {
            "belongs_to_set": False,
            "created_at": 1759845060482,
            "id": "b838d27b-cd5b-5647-8145-dcdffd120cb5",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "The Prince and Me tells the story of a down-to-earth college girl who unexpectedly ends up marrying a Danish prince after becoming his translator, navigating royal duties and personal growth.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759845060482,
            "version": 1
        },
        "bfae514a-cfed-5429-8295-a1db7a7e2241": {
            "belongs_to_set": False,
            "created_at": 1759845611147,
            "description": "American actress",
            "id": "bfae514a-cfed-5429-8295-a1db7a7e2241",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "kam heskin",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759845611147,
            "version": 1
        },
        "c24e3136-61f2-5c8c-a91f-c8e284f287d0": {
            "belongs_to_set": False,
            "created_at": 1759845987838,
            "description": "An actress who portrayed Elizabeth Bennet and Paige Morgan.",
            "id": "c24e3136-61f2-5c8c-a91f-c8e284f287d0",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "heskin",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759845987838,
            "version": 1
        },
        "c5abeb3a-352d-57ec-90b0-dd7f3df45e43": {
            "belongs_to_set": False,
            "created_at": 1759845987839,
            "description": "fictional character",
            "id": "c5abeb3a-352d-57ec-90b0-dd7f3df45e43",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "fictional character",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759845987839,
            "version": 1
        },
        "c7522338-9e72-54ad-aed4-3da4b196fa51": {
            "belongs_to_set": False,
            "created_at": 1759845987839,
            "description": "A character from Jane Austen's novel, portrayed by Heskin in a 2003 independent film.",
            "id": "c7522338-9e72-54ad-aed4-3da4b196fa51",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "elizabeth bennet",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759845987839,
            "version": 1
        },
        "d072ba0f-e1a9-58bf-9974-e1802adc8134": {
            "belongs_to_set": False,
            "created_at": 1759846689494,
            "description": "person",
            "id": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "person",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759846689494,
            "version": 1
        },
        "da5c5a02-b22e-510e-a8eb-0d65afe29447": {
            "belongs_to_set": False,
            "created_at": 1759846213522,
            "id": "da5c5a02-b22e-510e-a8eb-0d65afe29447",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Kam Heskin plays Paige Morgan in the 2004 film 'Saved!'",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759846213522,
            "version": 1
        },
        "daeabb25-9258-58f6-bc0f-d37c8b4bd6b2": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 79,
            "contains": [],
            "created_at": 1759845074046,
            "cut_type": "sentence_end",
            "id": "daeabb25-9258-58f6-bc0f-d37c8b4bd6b2",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "The Prince and Me is a 2004 romantic comedy film directed by Martha Coolidge, and starring Julia Stiles, Luke Mably, and Ben Miller, with Miranda Richardson, James Fox, and Alberta Watson.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759845074046,
            "version": 1
        },
        "dbf0acf5-9436-503e-8a6a-e8732d999b63": {
            "belongs_to_set": False,
            "created_at": 1759845550292,
            "external_metadata": "{}",
            "id": "dbf0acf5-9436-503e-8a6a-e8732d999b63",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "mime_type": "text/plain",
            "name": "text_e90368fc3d2373bd3c7bb487f20db2c3",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_e90368fc3d2373bd3c7bb487f20db2c3.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759845550292,
            "version": 1
        },
        "e35be8d4-845b-53a5-ab48-93bb7b7eca55": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 68,
            "created_at": 1759845854347,
            "cut_type": "sentence_end",
            "id": "e35be8d4-845b-53a5-ab48-93bb7b7eca55",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": " Heskin went to play Elizabeth Bennet in the 2003 independent film \"\", and Paige Morgan in the \"The Prince and Me\" film franchise (2006–2010).",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759845854347,
            "version": 1
        },
        "ec475bbf-f592-5f34-a3f6-3274a0b0edad": {
            "belongs_to_set": False,
            "created_at": 1759845296400,
            "id": "ec475bbf-f592-5f34-a3f6-3274a0b0edad",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "A romantic comedy film directed by Martha Coolidge featuring Julia Stiles, Luke Mably, Ben Miller, Miranda Richardson, James Fox, and Alberta Watson.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759845296400,
            "version": 1
        },
        "f767746b-8670-5dab-994a-38e9e3f20d2f": {
            "belongs_to_set": False,
            "created_at": 1759845539181,
            "id": "f767746b-8670-5dab-994a-38e9e3f20d2f",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Kam Heskin was an Australian film and television director known for his comedic work.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759845539181,
            "version": 1
        },
        "f85d905f-d729-5e66-a8c6-40fdac293138": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 25,
            "contains": [],
            "created_at": 1759846060763,
            "cut_type": "sentence_end",
            "id": "f85d905f-d729-5e66-a8c6-40fdac293138",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Kam Heskin plays Paige Morgan in which 2004 film?",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759846060763,
            "version": 1
        },
        "fb0219a0-2a36-5619-bfcb-533c08399cce": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 4,
            "created_at": 1759846368769,
            "cut_type": "sentence_cut",
            "id": "fb0219a0-2a36-5619-bfcb-533c08399cce",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "Martha Coolidge",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759846368769,
            "version": 1
        },
        "fece2b11-bd4d-502b-8e24-2b73649cf7b0": {
            "belongs_to_set": False,
            "chunk_index": 0,
            "chunk_size": 16,
            "created_at": 1759846233752,
            "cut_type": "sentence_end",
            "id": "fece2b11-bd4d-502b-8e24-2b73649cf7b0",
            "metadata": {
                "index_fields": [
                    "text"
                ]
            },
            "name": "",
            "ontology_valid": False,
            "text": "The Prince and Me is directed by who?",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759846233752,
            "version": 1
        },
        "fee17662-f962-5bba-ab3c-1f889a7a6b40": {
            "belongs_to_set": False,
            "created_at": 1759846313687,
            "description": "movie",
            "id": "fee17662-f962-5bba-ab3c-1f889a7a6b40",
            "metadata": {
                "index_fields": [
                    "name"
                ]
            },
            "name": "movie",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759846313687,
            "version": 1
        }
    },
    "edges": 
    {
        "edge1": {
            "label": "is_part_of",
            "source": "9ade0e79-6d39-530e-baeb-1d1b3048bffe",
            "target": "a1b1f51e-1bd3-551b-bd4a-fe311a7f9b22"
        },
        "edge10": {
            "label": "made_from",
            "source": "b838d27b-cd5b-5647-8145-dcdffd120cb5",
            "target": "9ade0e79-6d39-530e-baeb-1d1b3048bffe"
        },
        "edge11": {
            "label": "is_part_of",
            "source": "daeabb25-9258-58f6-bc0f-d37c8b4bd6b2",
            "target": "684c67fa-ef22-5a85-aa3a-ae377468c50a"
        },
        "edge12": {
            "label": "made_from",
            "source": "ec475bbf-f592-5f34-a3f6-3274a0b0edad",
            "target": "daeabb25-9258-58f6-bc0f-d37c8b4bd6b2"
        },
        "edge13": {
            "label": "is_part_of",
            "source": "3fde779e-ee6d-5470-9839-3752302cbca4",
            "target": "ae78912d-86ba-546c-a560-1074c1f53797"
        },
        "edge14": {
            "label": "made_from",
            "source": "a4596b20-7262-5555-b44b-52c3438ee8da",
            "target": "3fde779e-ee6d-5470-9839-3752302cbca4"
        },
        "edge15": {
            "label": "is_part_of",
            "source": "6905fcf3-7497-510a-95b0-c26368ec4a3e",
            "target": "703f131a-8a0d-5747-803f-9294267118f6"
        },
        "edge16": {
            "label": "contains",
            "source": "6905fcf3-7497-510a-95b0-c26368ec4a3e",
            "target": "bfae514a-cfed-5429-8295-a1db7a7e2241"
        },
        "edge17": {
            "label": "is_a",
            "source": "bfae514a-cfed-5429-8295-a1db7a7e2241",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge18": {
            "label": "made_from",
            "source": "f767746b-8670-5dab-994a-38e9e3f20d2f",
            "target": "6905fcf3-7497-510a-95b0-c26368ec4a3e"
        },
        "edge19": {
            "label": "contains",
            "source": "3883cc14-afe1-574b-9cae-3925628fb5da",
            "target": "bfae514a-cfed-5429-8295-a1db7a7e2241"
        },
        "edge2": {
            "label": "contains",
            "source": "9ade0e79-6d39-530e-baeb-1d1b3048bffe",
            "target": "6a15b02f-0712-56dc-a290-915475d29abb"
        },
        "edge20": {
            "label": "is_part_of",
            "source": "3883cc14-afe1-574b-9cae-3925628fb5da",
            "target": "dbf0acf5-9436-503e-8a6a-e8732d999b63"
        },
        "edge21": {
            "label": "made_from",
            "source": "3b66f5d8-8c09-5992-a61f-dbcb5e5e4535",
            "target": "3883cc14-afe1-574b-9cae-3925628fb5da"
        },
        "edge22": {
            "label": "is_part_of",
            "source": "688654a6-42be-5e71-b426-6231f483da19",
            "target": "5811d8f7-e0a7-555f-9066-b81c0f6c9ad0"
        },
        "edge23": {
            "label": "made_from",
            "source": "b234338e-a3a0-590e-ba4c-26f363e04f9e",
            "target": "688654a6-42be-5e71-b426-6231f483da19"
        },
        "edge24": {
            "label": "is_part_of",
            "source": "e35be8d4-845b-53a5-ab48-93bb7b7eca55",
            "target": "30ca42a3-ec5a-59d3-9228-0da4f454be03"
        },
        "edge25": {
            "label": "contains",
            "source": "e35be8d4-845b-53a5-ab48-93bb7b7eca55",
            "target": "c24e3136-61f2-5c8c-a91f-c8e284f287d0"
        },
        "edge26": {
            "label": "contains",
            "source": "e35be8d4-845b-53a5-ab48-93bb7b7eca55",
            "target": "c7522338-9e72-54ad-aed4-3da4b196fa51"
        },
        "edge27": {
            "label": "contains",
            "source": "e35be8d4-845b-53a5-ab48-93bb7b7eca55",
            "target": "485c3abe-cbe6-53c6-8b46-d9e475d02493"
        },
        "edge28": {
            "label": "contains",
            "source": "e35be8d4-845b-53a5-ab48-93bb7b7eca55",
            "target": "66127932-b89f-5cac-bfb3-8132b4119cbd"
        },
        "edge29": {
            "label": "is_a",
            "source": "c24e3136-61f2-5c8c-a91f-c8e284f287d0",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge3": {
            "label": "contains",
            "source": "9ade0e79-6d39-530e-baeb-1d1b3048bffe",
            "target": "1840d0e8-63ef-56a5-ab57-974d1557da19"
        },
        "edge30": {
            "label": "acted_as_ellizabeth_bennet_in_film",
            "source": "c24e3136-61f2-5c8c-a91f-c8e284f287d0",
            "target": "c7522338-9e72-54ad-aed4-3da4b196fa51"
        },
        "edge31": {
            "label": "acted_in",
            "source": "c24e3136-61f2-5c8c-a91f-c8e284f287d0",
            "target": "485c3abe-cbe6-53c6-8b46-d9e475d02493"
        },
        "edge32": {
            "label": "played_char_paige_morgan",
            "source": "c24e3136-61f2-5c8c-a91f-c8e284f287d0",
            "target": "66127932-b89f-5cac-bfb3-8132b4119cbd"
        },
        "edge33": {
            "label": "is_a",
            "source": "c7522338-9e72-54ad-aed4-3da4b196fa51",
            "target": "c5abeb3a-352d-57ec-90b0-dd7f3df45e43"
        },
        "edge34": {
            "label": "is_a",
            "source": "485c3abe-cbe6-53c6-8b46-d9e475d02493",
            "target": "b630e5b0-ae6d-55d0-99fd-039d9e9b5e2b"
        },
        "edge35": {
            "label": "is_a",
            "source": "66127932-b89f-5cac-bfb3-8132b4119cbd",
            "target": "c5abeb3a-352d-57ec-90b0-dd7f3df45e43"
        },
        "edge36": {
            "label": "made_from",
            "source": "adba7583-35a0-5239-b4e4-4d34987afcd0",
            "target": "e35be8d4-845b-53a5-ab48-93bb7b7eca55"
        },
        "edge37": {
            "label": "is_part_of",
            "source": "f85d905f-d729-5e66-a8c6-40fdac293138",
            "target": "2c0ab9d2-2991-5742-b083-4747f1c55110"
        },
        "edge38": {
            "label": "made_from",
            "source": "da5c5a02-b22e-510e-a8eb-0d65afe29447",
            "target": "f85d905f-d729-5e66-a8c6-40fdac293138"
        },
        "edge39": {
            "label": "is_part_of",
            "source": "fece2b11-bd4d-502b-8e24-2b73649cf7b0",
            "target": "3adcf22e-4932-59a0-899e-1b281fa4112b"
        },
        "edge4": {
            "label": "contains",
            "source": "9ade0e79-6d39-530e-baeb-1d1b3048bffe",
            "target": "7ea1b82c-cbfd-52d2-8058-ba9ca0aca9d0"
        },
        "edge40": {
            "label": "contains",
            "source": "fece2b11-bd4d-502b-8e24-2b73649cf7b0",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge41": {
            "label": "contains",
            "source": "fece2b11-bd4d-502b-8e24-2b73649cf7b0",
            "target": "1c877e38-afdb-5af9-bfa1-c14235256bbe"
        },
        "edge42": {
            "label": "is_a",
            "source": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "target": "fee17662-f962-5bba-ab3c-1f889a7a6b40"
        },
        "edge43": {
            "label": "directed_by",
            "source": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "target": "1c877e38-afdb-5af9-bfa1-c14235256bbe"
        },
        "edge44": {
            "label": "is_a",
            "source": "1c877e38-afdb-5af9-bfa1-c14235256bbe",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge45": {
            "label": "made_from",
            "source": "8598f90c-7a18-5742-85f6-3fd9a634a6d9",
            "target": "fece2b11-bd4d-502b-8e24-2b73649cf7b0"
        },
        "edge46": {
            "label": "contains",
            "source": "fb0219a0-2a36-5619-bfcb-533c08399cce",
            "target": "1c877e38-afdb-5af9-bfa1-c14235256bbe"
        },
        "edge47": {
            "label": "is_part_of",
            "source": "fb0219a0-2a36-5619-bfcb-533c08399cce",
            "target": "39c2c48c-c248-5c33-a4d2-c93b3d4f4405"
        },
        "edge48": {
            "label": "made_from",
            "source": "36bbddca-8ba0-5775-835e-3def224b6b8e",
            "target": "fb0219a0-2a36-5619-bfcb-533c08399cce"
        },
        "edge49": {
            "label": "contains",
            "source": "ae518edb-8a59-5df3-9110-2aaf587e57c8",
            "target": "1c877e38-afdb-5af9-bfa1-c14235256bbe"
        },
        "edge5": {
            "label": "is_a",
            "source": "6a15b02f-0712-56dc-a290-915475d29abb",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge50": {
            "label": "is_part_of",
            "source": "ae518edb-8a59-5df3-9110-2aaf587e57c8",
            "target": "531b59b2-3eff-5061-8537-efe0f3921d44"
        },
        "edge51": {
            "label": "made_from",
            "source": "66a4cf94-2589-5171-b6e9-82702cc1eaf8",
            "target": "ae518edb-8a59-5df3-9110-2aaf587e57c8"
        },
        "edge52": {
            "label": "is_part_of",
            "source": "7869eb3c-9c39-5f17-ac04-61fb5ab1076d",
            "target": "2faae991-8084-59f4-becd-e6417659176a"
        },
        "edge53": {
            "label": "contains",
            "source": "7869eb3c-9c39-5f17-ac04-61fb5ab1076d",
            "target": "818506fc-19bc-5fc0-8f96-f0a564a54ff4"
        },
        "edge54": {
            "label": "contains",
            "source": "7869eb3c-9c39-5f17-ac04-61fb5ab1076d",
            "target": "3799a3e5-bbf2-560a-86ac-d306bff33be9"
        },
        "edge55": {
            "label": "is_a",
            "source": "818506fc-19bc-5fc0-8f96-f0a564a54ff4",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge56": {
            "label": "published_in",
            "source": "818506fc-19bc-5fc0-8f96-f0a564a54ff4",
            "target": "3799a3e5-bbf2-560a-86ac-d306bff33be9"
        },
        "edge57": {
            "label": "is_a",
            "source": "3799a3e5-bbf2-560a-86ac-d306bff33be9",
            "target": "3d18f258-7e29-50c1-b3dc-4874c7ee86fa"
        },
        "edge58": {
            "label": "made_from",
            "source": "2d894c54-6215-58c2-878b-5258ae2a688a",
            "target": "7869eb3c-9c39-5f17-ac04-61fb5ab1076d"
        },
        "edge6": {
            "label": "accidentally_saves",
            "source": "6a15b02f-0712-56dc-a290-915475d29abb",
            "target": "1840d0e8-63ef-56a5-ab57-974d1557da19"
        },
        "edge7": {
            "label": "is_a",
            "source": "1840d0e8-63ef-56a5-ab57-974d1557da19",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge8": {
            "label": "parent_of",
            "source": "1840d0e8-63ef-56a5-ab57-974d1557da19",
            "target": "7ea1b82c-cbfd-52d2-8058-ba9ca0aca9d0"
        },
        "edge9": {
            "label": "is_a",
            "source": "7ea1b82c-cbfd-52d2-8058-ba9ca0aca9d0",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        }
    }
}

FIXED_RESULT2 = {
    "final_answer": "The director of 'The Prince and Me' is Martha Coolidge. Her first name is Martha. The first letter of her first name is M, and the last letter is a. There are four letters (a-r-t-h) between the M and a.",
    "nodes": 
    {
        "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc": {
            "created_at": 1759847372239,
            "description": "Acted in 'The Prince and Me'.",
            "id": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "ben miller",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847415051,
            "version": 1
        },
        "1b04e0d5-1c1d-5d20-9213-9c0416c64156": {
            "created_at": 1759847768325,
            "id": "1b04e0d5-1c1d-5d20-9213-9c0416c64156",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin is an American actress born on May 8, 1973.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759847773772,
            "version": 1
        },
        "1b12b5bd-89ef-5ae5-b757-578011cfd7e3": {
            "created_at": 1759847125680,
            "description": "American actress and producer known for roles in romantic comedies.",
            "id": "1b12b5bd-89ef-5ae5-b757-578011cfd7e3",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "rachel mcadams",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847178306,
            "version": 1
        },
        "1c877e38-afdb-5af9-bfa1-c14235256bbe": {
            "created_at": 1759847372239,
            "description": "Directed 'The Prince and Me'.",
            "id": "1c877e38-afdb-5af9-bfa1-c14235256bbe",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "martha coolidge",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847415051,
            "version": 1
        },
        "21d19d74-b14b-5c0a-9272-20904a2f8c73": {
            "created_at": 1759847511190,
            "description": "Pretends to be a normal college student",
            "id": "21d19d74-b14b-5c0a-9272-20904a2f8c73",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "prince",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847547293,
            "version": 1
        },
        "2a90b479-03f1-5c91-98a7-e9cc71f059f0": {
            "created_at": 1759847511190,
            "description": "The educational institution where the story is set",
            "id": "2a90b479-03f1-5c91-98a7-e9cc71f059f0",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "wisconsin college",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847547293,
            "version": 1
        },
        "2e52a8dc-f4a7-56a0-abed-c019f8da2bc4": {
            "created_at": 1759847184411,
            "external_metadata": "{}",
            "id": "2e52a8dc-f4a7-56a0-abed-c019f8da2bc4",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_0d8bce0ea5edd9bf132de26723b43b94",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_0d8bce0ea5edd9bf132de26723b43b94.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759847415051,
            "version": 1
        },
        "382a043d-4883-544b-bf6d-f26a38ecadf5": {
            "chunk_index": 0,
            "chunk_size": 7,
            "created_at": 1759847009325,
            "cut_type": "sentence_cut",
            "id": "382a043d-4883-544b-bf6d-f26a38ecadf5",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759847178306,
            "version": 1
        },
        "3c231025-e63e-52ea-a0ce-01e4cfc7e8a1": {
            "created_at": 1759847646010,
            "id": "3c231025-e63e-52ea-a0ce-01e4cfc7e8a1",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin is a character known for their expertise in disguise and espionage.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759847650973,
            "version": 1
        },
        "4468500a-9b73-5cba-a18c-f14081b34072": {
            "chunk_index": 0,
            "chunk_size": 79,
            "created_at": 1759847185574,
            "cut_type": "sentence_end",
            "id": "4468500a-9b73-5cba-a18c-f14081b34072",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me is a 2004 romantic comedy film directed by Martha Coolidge, and starring Julia Stiles, Luke Mably, and Ben Miller, with Miranda Richardson, James Fox, and Alberta Watson.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759847415051,
            "version": 1
        },
        "48355aef-4600-5836-a677-65d05d620689": {
            "created_at": 1759847372239,
            "description": "Acted in 'The Prince and Me'.",
            "id": "48355aef-4600-5836-a677-65d05d620689",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "miranda richardson",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847415051,
            "version": 1
        },
        "4ff4542b-e96c-5bb4-8f63-181b16e15c44": {
            "chunk_index": 0,
            "chunk_size": 56,
            "created_at": 1759847422270,
            "cut_type": "sentence_end",
            "id": "4ff4542b-e96c-5bb4-8f63-181b16e15c44",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": " The film focuses on Paige Morgan, a pre-med college student in Wisconsin, who is pursued by a prince posing as a normal college student.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759847547293,
            "version": 1
        },
        "5497eae1-bb90-5e70-8ca1-23dab5acbd83": {
            "created_at": 1759847171762,
            "id": "5497eae1-bb90-5e70-8ca1-23dab5acbd83",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me is a romantic comedy about a down-to-earth American woman named Paige who becomes engaged to a Danish prince. The film humorously explores cultural differences, royal duties, and romantic challenges between them.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759847178306,
            "version": 1
        },
        "5f710d9d-8811-5cfb-9175-c5c0533b82ca": {
            "created_at": 1759847372238,
            "description": "film",
            "id": "5f710d9d-8811-5cfb-9175-c5c0533b82ca",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "film",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759847415051,
            "version": 1
        },
        "6531474e-29a2-51fb-b637-5715662c596c": {
            "created_at": 1759847780086,
            "external_metadata": "{}",
            "id": "6531474e-29a2-51fb-b637-5715662c596c",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_01a827d5156ebe7bf6384321dae464f9",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_01a827d5156ebe7bf6384321dae464f9.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759847961794,
            "version": 1
        },
        "664d4c41-2b73-5130-9001-35cb8940b2b5": {
            "created_at": 1759847372239,
            "description": "Acted in 'The Prince and Me'.",
            "id": "664d4c41-2b73-5130-9001-35cb8940b2b5",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "alberta watson",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847415051,
            "version": 1
        },
        "70438052-4b09-5519-b6cd-8109c32ad6d5": {
            "created_at": 1759847968126,
            "external_metadata": "{}",
            "id": "70438052-4b09-5519-b6cd-8109c32ad6d5",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_986e4ef18b400a6074fc04116fc4f4bd",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_986e4ef18b400a6074fc04116fc4f4bd.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759848176096,
            "version": 1
        },
        "80833b75-680c-546c-a49e-23d8d844d715": {
            "created_at": 1759847511189,
            "description": "Pre-med college student",
            "id": "80833b75-680c-546c-a49e-23d8d844d715",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "paige morgan",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847547293,
            "version": 1
        },
        "838b29ab-a914-599f-b164-d5f76d619347": {
            "created_at": 1759847953956,
            "id": "838b29ab-a914-599f-b164-d5f76d619347",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "This passage outlines an actress's early career, starting with her role as Caitlin Richards Deschanel on 'Sunset Beach' (1998–1999), and subsequently appearing in major films such as 'Planet of the Apes' (2001) and 'Catch Me If You Can' (2002).",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759847961794,
            "version": 1
        },
        "87b90780-ba84-50e2-a755-23e6d86cfe4c": {
            "created_at": 1759847372238,
            "description": "A 2004 romantic comedy film directed by Martha Coolidge.",
            "id": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "the prince and me",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847415051,
            "version": 1
        },
        "96d41bf3-11c9-50c5-9094-a27db839e3d7": {
            "created_at": 1759847372239,
            "description": "Acted in 'The Prince and Me'.",
            "id": "96d41bf3-11c9-50c5-9094-a27db839e3d7",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "james fox",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847415051,
            "version": 1
        },
        "a42603f2-e598-59b6-ac4f-71e6ac533c07": {
            "created_at": 1759847008140,
            "external_metadata": "{}",
            "id": "a42603f2-e598-59b6-ac4f-71e6ac533c07",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_253becda393cc4221094e8eb3cabf879",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_253becda393cc4221094e8eb3cabf879.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759847178306,
            "version": 1
        },
        "a7cedbc1-1a61-5d1a-9136-a49b5cc9e7f2": {
            "chunk_index": 0,
            "chunk_size": 41,
            "contains": [],
            "created_at": 1759847658504,
            "cut_type": "sentence_end",
            "id": "a7cedbc1-1a61-5d1a-9136-a49b5cc9e7f2",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin (born Kam Erika Heskin on May 8, 1973) is an American actress.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759847773772,
            "version": 1
        },
        "ae5586aa-4061-5941-95e2-949bb14a1d94": {
            "chunk_index": 0,
            "chunk_size": 101,
            "contains": [],
            "created_at": 1759847781214,
            "cut_type": "sentence_end",
            "id": "ae5586aa-4061-5941-95e2-949bb14a1d94",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": " She began her career playing Caitlin Richards Deschanel on the NBC daytime soap opera \"Sunset Beach\" (1998–1999), before appearing in films \"Planet of the Apes\" (2001 and \"Catch Me If You Can\" (2002).",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759847961794,
            "version": 1
        },
        "b8401a9b-121e-5571-9ad5-549acf6c5714": {
            "created_at": 1759847125680,
            "description": "English actor, producer, host, and activist known for his roles in romantic comedies like Notting Hill.",
            "id": "b8401a9b-121e-5571-9ad5-549acf6c5714",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "hugh grant",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847178306,
            "version": 1
        },
        "b8ecef91-f5e5-52cd-865d-706c00eaa020": {
            "created_at": 1759847421124,
            "external_metadata": "{}",
            "id": "b8ecef91-f5e5-52cd-865d-706c00eaa020",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_be7a9849b7da3fe3ac22de8ce398250d",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_be7a9849b7da3fe3ac22de8ce398250d.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759847547293,
            "version": 1
        },
        "bfae514a-cfed-5429-8295-a1db7a7e2241": {
            "created_at": 1759847611875,
            "description": "A professional in marketing and data analytics, known for contributions to modern marketing practices.",
            "id": "bfae514a-cfed-5429-8295-a1db7a7e2241",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "kam heskin",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847650973,
            "version": 1
        },
        "c4d03ab9-9842-55a6-bfe6-b6ac7ce06a6c": {
            "chunk_index": 0,
            "chunk_size": 68,
            "contains": [],
            "created_at": 1759847969253,
            "cut_type": "sentence_end",
            "id": "c4d03ab9-9842-55a6-bfe6-b6ac7ce06a6c",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": " Heskin went to play Elizabeth Bennet in the 2003 independent film \"\", and Paige Morgan in the \"The Prince and Me\" film franchise (2006–2010).",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759848176096,
            "version": 1
        },
        "ca7a09a3-29e9-5558-b3c5-c33399f03b88": {
            "created_at": 1759847541663,
            "id": "ca7a09a3-29e9-5558-b3c5-c33399f03b88",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The film centers on Paige Morgan.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759847547293,
            "version": 1
        },
        "cae97d8e-77ee-5de2-b64f-05ebfd47d371": {
            "created_at": 1759847408071,
            "id": "cae97d8e-77ee-5de2-b64f-05ebfd47d371",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me is a romantic comedy film.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759847415051,
            "version": 1
        },
        "ccbee186-a5fc-55a2-ad68-2bbe3f237b80": {
            "chunk_index": 0,
            "chunk_size": 5,
            "created_at": 1759847554726,
            "cut_type": "sentence_cut",
            "id": "ccbee186-a5fc-55a2-ad68-2bbe3f237b80",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759847650973,
            "version": 1
        },
        "cd73159f-5997-55bd-932c-73c0f2340291": {
            "created_at": 1759847553615,
            "external_metadata": "{}",
            "id": "cd73159f-5997-55bd-932c-73c0f2340291",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_c848f59aad5b304add1773efba5b0762",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_c848f59aad5b304add1773efba5b0762.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759847650973,
            "version": 1
        },
        "d072ba0f-e1a9-58bf-9974-e1802adc8134": {
            "created_at": 1759847611875,
            "description": "person",
            "id": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "person",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759847650973,
            "version": 1
        },
        "d3d7b6b4-9b0d-52e8-9e09-a9e9cf4b5a4d": {
            "created_at": 1759847511190,
            "description": "organization",
            "id": "d3d7b6b4-9b0d-52e8-9e09-a9e9cf4b5a4d",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "organization",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759847547293,
            "version": 1
        },
        "d8241703-7dcf-596e-8095-a659b7ee31af": {
            "created_at": 1759847657289,
            "external_metadata": "{}",
            "id": "d8241703-7dcf-596e-8095-a659b7ee31af",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_e90368fc3d2373bd3c7bb487f20db2c3",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_e90368fc3d2373bd3c7bb487f20db2c3.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759847773772,
            "version": 1
        },
        "ed0c0811-3a61-52c6-aa9b-2dacd5e85fc1": {
            "created_at": 1759848170033,
            "id": "ed0c0811-3a61-52c6-aa9b-2dacd5e85fc1",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Heston went on to portray Elizabeth Bennet in the 2003 independent film 'The Modern Bridget Jones' and Paige Morgan in the 'The Prince and Me' series (2006–2010).",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759848176096,
            "version": 1
        },
        "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0": {
            "created_at": 1759847372239,
            "description": "Acted in 'The Prince and Me'.",
            "id": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "julia stiles",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847415051,
            "version": 1
        },
        "f7210df6-380d-597c-a594-72ee0854a798": {
            "created_at": 1759847372239,
            "description": "Acted in 'The Prince and Me'.",
            "id": "f7210df6-380d-597c-a594-72ee0854a798",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "luke mably",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847415051,
            "version": 1
        },
        "fb8e5a23-19c1-5dd7-92fd-081476f9814a": {
            "created_at": 1759847125680,
            "description": "Canadian-American actress known for her work in both films and television.",
            "id": "fb8e5a23-19c1-5dd7-92fd-081476f9814a",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "heather graham",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759847178306,
            "version": 1
        },
        "fee17662-f962-5bba-ab3c-1f889a7a6b40": {
            "created_at": 1759847125680,
            "description": "movie",
            "id": "fee17662-f962-5bba-ab3c-1f889a7a6b40",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "movie",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759847178306,
            "version": 1
        }
    },
    "edges": 
    {
        "edge1": {
            "label": "contains",
            "source": "382a043d-4883-544b-bf6d-f26a38ecadf5",
            "target": "1b12b5bd-89ef-5ae5-b757-578011cfd7e3"
        },
        "edge10": {
            "label": "acted_in",
            "source": "1b12b5bd-89ef-5ae5-b757-578011cfd7e3",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge11": {
            "label": "acted_in",
            "source": "fb8e5a23-19c1-5dd7-92fd-081476f9814a",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge12": {
            "label": "acted_in",
            "source": "b8401a9b-121e-5571-9ad5-549acf6c5714",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge13": {
            "label": "made_from",
            "source": "5497eae1-bb90-5e70-8ca1-23dab5acbd83",
            "target": "382a043d-4883-544b-bf6d-f26a38ecadf5"
        },
        "edge14": {
            "label": "contains",
            "source": "4468500a-9b73-5cba-a18c-f14081b34072",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge15": {
            "label": "is_a",
            "source": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "target": "5f710d9d-8811-5cfb-9175-c5c0533b82ca"
        },
        "edge16": {
            "label": "contains",
            "source": "4468500a-9b73-5cba-a18c-f14081b34072",
            "target": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0"
        },
        "edge17": {
            "label": "is_a",
            "source": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge18": {
            "label": "contains",
            "source": "4468500a-9b73-5cba-a18c-f14081b34072",
            "target": "f7210df6-380d-597c-a594-72ee0854a798"
        },
        "edge19": {
            "label": "is_a",
            "source": "f7210df6-380d-597c-a594-72ee0854a798",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge2": {
            "label": "is_a",
            "source": "1b12b5bd-89ef-5ae5-b757-578011cfd7e3",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge20": {
            "label": "contains",
            "source": "4468500a-9b73-5cba-a18c-f14081b34072",
            "target": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc"
        },
        "edge21": {
            "label": "is_a",
            "source": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge22": {
            "label": "contains",
            "source": "4468500a-9b73-5cba-a18c-f14081b34072",
            "target": "1c877e38-afdb-5af9-bfa1-c14235256bbe"
        },
        "edge23": {
            "label": "is_a",
            "source": "1c877e38-afdb-5af9-bfa1-c14235256bbe",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge24": {
            "label": "contains",
            "source": "4468500a-9b73-5cba-a18c-f14081b34072",
            "target": "48355aef-4600-5836-a677-65d05d620689"
        },
        "edge25": {
            "label": "is_a",
            "source": "48355aef-4600-5836-a677-65d05d620689",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge26": {
            "label": "contains",
            "source": "4468500a-9b73-5cba-a18c-f14081b34072",
            "target": "96d41bf3-11c9-50c5-9094-a27db839e3d7"
        },
        "edge27": {
            "label": "is_a",
            "source": "96d41bf3-11c9-50c5-9094-a27db839e3d7",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge28": {
            "label": "contains",
            "source": "4468500a-9b73-5cba-a18c-f14081b34072",
            "target": "664d4c41-2b73-5130-9001-35cb8940b2b5"
        },
        "edge29": {
            "label": "is_a",
            "source": "664d4c41-2b73-5130-9001-35cb8940b2b5",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge3": {
            "label": "contains",
            "source": "382a043d-4883-544b-bf6d-f26a38ecadf5",
            "target": "fb8e5a23-19c1-5dd7-92fd-081476f9814a"
        },
        "edge30": {
            "label": "is_part_of",
            "source": "4468500a-9b73-5cba-a18c-f14081b34072",
            "target": "2e52a8dc-f4a7-56a0-abed-c019f8da2bc4"
        },
        "edge31": {
            "label": "acted_in",
            "source": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge32": {
            "label": "acted_in",
            "source": "f7210df6-380d-597c-a594-72ee0854a798",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge33": {
            "label": "acted_in",
            "source": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge34": {
            "label": "directed",
            "source": "1c877e38-afdb-5af9-bfa1-c14235256bbe",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge35": {
            "label": "acted_in",
            "source": "48355aef-4600-5836-a677-65d05d620689",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge36": {
            "label": "acted_in",
            "source": "96d41bf3-11c9-50c5-9094-a27db839e3d7",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge37": {
            "label": "acted_in",
            "source": "664d4c41-2b73-5130-9001-35cb8940b2b5",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge38": {
            "label": "made_from",
            "source": "cae97d8e-77ee-5de2-b64f-05ebfd47d371",
            "target": "4468500a-9b73-5cba-a18c-f14081b34072"
        },
        "edge39": {
            "label": "contains",
            "source": "4ff4542b-e96c-5bb4-8f63-181b16e15c44",
            "target": "80833b75-680c-546c-a49e-23d8d844d715"
        },
        "edge4": {
            "label": "is_a",
            "source": "fb8e5a23-19c1-5dd7-92fd-081476f9814a",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge40": {
            "label": "is_a",
            "source": "80833b75-680c-546c-a49e-23d8d844d715",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge41": {
            "label": "contains",
            "source": "4ff4542b-e96c-5bb4-8f63-181b16e15c44",
            "target": "21d19d74-b14b-5c0a-9272-20904a2f8c73"
        },
        "edge42": {
            "label": "is_a",
            "source": "21d19d74-b14b-5c0a-9272-20904a2f8c73",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge43": {
            "label": "contains",
            "source": "4ff4542b-e96c-5bb4-8f63-181b16e15c44",
            "target": "2a90b479-03f1-5c91-98a7-e9cc71f059f0"
        },
        "edge44": {
            "label": "is_a",
            "source": "2a90b479-03f1-5c91-98a7-e9cc71f059f0",
            "target": "d3d7b6b4-9b0d-52e8-9e09-a9e9cf4b5a4d"
        },
        "edge45": {
            "label": "is_part_of",
            "source": "4ff4542b-e96c-5bb4-8f63-181b16e15c44",
            "target": "b8ecef91-f5e5-52cd-865d-706c00eaa020"
        },
        "edge46": {
            "label": "attends_college",
            "source": "80833b75-680c-546c-a49e-23d8d844d715",
            "target": "2a90b479-03f1-5c91-98a7-e9cc71f059f0"
        },
        "edge47": {
            "label": "is_attending_college_as",
            "source": "21d19d74-b14b-5c0a-9272-20904a2f8c73",
            "target": "2a90b479-03f1-5c91-98a7-e9cc71f059f0"
        },
        "edge48": {
            "label": "made_from",
            "source": "ca7a09a3-29e9-5558-b3c5-c33399f03b88",
            "target": "4ff4542b-e96c-5bb4-8f63-181b16e15c44"
        },
        "edge49": {
            "label": "contains",
            "source": "ccbee186-a5fc-55a2-ad68-2bbe3f237b80",
            "target": "bfae514a-cfed-5429-8295-a1db7a7e2241"
        },
        "edge5": {
            "label": "contains",
            "source": "382a043d-4883-544b-bf6d-f26a38ecadf5",
            "target": "b8401a9b-121e-5571-9ad5-549acf6c5714"
        },
        "edge50": {
            "label": "is_a",
            "source": "bfae514a-cfed-5429-8295-a1db7a7e2241",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge51": {
            "label": "is_part_of",
            "source": "ccbee186-a5fc-55a2-ad68-2bbe3f237b80",
            "target": "cd73159f-5997-55bd-932c-73c0f2340291"
        },
        "edge52": {
            "label": "made_from",
            "source": "3c231025-e63e-52ea-a0ce-01e4cfc7e8a1",
            "target": "ccbee186-a5fc-55a2-ad68-2bbe3f237b80"
        },
        "edge53": {
            "label": "is_part_of",
            "source": "a7cedbc1-1a61-5d1a-9136-a49b5cc9e7f2",
            "target": "d8241703-7dcf-596e-8095-a659b7ee31af"
        },
        "edge54": {
            "label": "made_from",
            "source": "1b04e0d5-1c1d-5d20-9213-9c0416c64156",
            "target": "a7cedbc1-1a61-5d1a-9136-a49b5cc9e7f2"
        },
        "edge55": {
            "label": "is_part_of",
            "source": "ae5586aa-4061-5941-95e2-949bb14a1d94",
            "target": "6531474e-29a2-51fb-b637-5715662c596c"
        },
        "edge56": {
            "label": "made_from",
            "source": "838b29ab-a914-599f-b164-d5f76d619347",
            "target": "ae5586aa-4061-5941-95e2-949bb14a1d94"
        },
        "edge57": {
            "label": "is_part_of",
            "source": "c4d03ab9-9842-55a6-bfe6-b6ac7ce06a6c",
            "target": "70438052-4b09-5519-b6cd-8109c32ad6d5"
        },
        "edge58": {
            "label": "made_from",
            "source": "ed0c0811-3a61-52c6-aa9b-2dacd5e85fc1",
            "target": "c4d03ab9-9842-55a6-bfe6-b6ac7ce06a6c"
        },
        "edge6": {
            "label": "is_a",
            "source": "b8401a9b-121e-5571-9ad5-549acf6c5714",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge7": {
            "label": "contains",
            "source": "382a043d-4883-544b-bf6d-f26a38ecadf5",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge8": {
            "label": "is_a",
            "source": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "target": "fee17662-f962-5bba-ab3c-1f889a7a6b40"
        },
        "edge9": {
            "label": "is_part_of",
            "source": "382a043d-4883-544b-bf6d-f26a38ecadf5",
            "target": "a42603f2-e598-59b6-ac4f-71e6ac533c07"
        }
    }
}

FIXED_RESULT3 = {
    "final_answer": "To determine how many letters are between the first and last letters of the first name of the director of a 2004 film where Kam Heskin plays Paige Morgan, we can deduce from the knowledge graph:\\n\\n1. The movie in which Kam Heskin plays Paige Morgan is \\'The Prince and Me\\', released in 2004.\\n2. According to the nodes, \"Martha Coolidge\" directed this film.\\n3. Considering Martha\\'s first name — \\'Martha\\':\\n   - First letter: M\\n   - Last letter: A\\n   - Letters in between: r, t, h (three letters)\\n\\nTherefore, there are 3 letters between the first and last letters of \\'Martha\\'.",
    "nodes": 
    {
        "00ba6221-07c8-5f26-bae3-c0e79f2ff783": {
            "chunk_index": 0,
            "chunk_size": 56,
            "contains": [],
            "created_at": 1759863762312,
            "cut_type": "sentence_end",
            "id": "00ba6221-07c8-5f26-bae3-c0e79f2ff783",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": " The film focuses on Paige Morgan, a pre-med college student in Wisconsin, who is pursued by a prince posing as a normal college student.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759863888214,
            "version": 1
        },
        "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc": {
            "created_at": 1759863710271,
            "description": "Actor starring in 'The Prince and Me'.",
            "id": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "ben miller",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759863754879,
            "version": 1
        },
        "0f7c3e65-da98-57aa-9793-3919242b7edb": {
            "created_at": 1759864001424,
            "id": "0f7c3e65-da98-57aa-9793-3919242b7edb",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin is a prominent figure known for his work as an educator, author, and motivational speaker.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759864007223,
            "version": 1
        },
        "1c877e38-afdb-5af9-bfa1-c14235256bbe": {
            "created_at": 1759863710271,
            "description": "Director of the movie 'The Prince and Me'.",
            "id": "1c877e38-afdb-5af9-bfa1-c14235256bbe",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "martha coolidge",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759863754879,
            "version": 1
        },
        "27a88ae9-bd27-5e0b-a5c4-064ca1b72ee2": {
            "created_at": 1759864165646,
            "external_metadata": "{}",
            "id": "27a88ae9-bd27-5e0b-a5c4-064ca1b72ee2",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_01a827d5156ebe7bf6384321dae464f9",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_01a827d5156ebe7bf6384321dae464f9.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759864348157,
            "version": 1
        },
        "43e98278-8388-5c90-ab26-e59b77c0a8d1": {
            "chunk_index": 0,
            "chunk_size": 7,
            "contains": [],
            "created_at": 1759863406596,
            "cut_type": "sentence_cut",
            "id": "43e98278-8388-5c90-ab26-e59b77c0a8d1",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759863517064,
            "version": 1
        },
        "44d222d6-0a45-5a61-a030-dd082df76979": {
            "chunk_index": 0,
            "chunk_size": 41,
            "created_at": 1759864014715,
            "cut_type": "sentence_end",
            "id": "44d222d6-0a45-5a61-a030-dd082df76979",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin (born Kam Erika Heskin on May 8, 1973) is an American actress.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759864159218,
            "version": 1
        },
        "48355aef-4600-5836-a677-65d05d620689": {
            "created_at": 1759863710274,
            "description": "Actress featured in 'The Prince and Me'.",
            "id": "48355aef-4600-5836-a677-65d05d620689",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "miranda richardson",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759863754879,
            "version": 1
        },
        "48df3a78-2989-5a93-bcfc-c00bbf2626d4": {
            "created_at": 1759864116781,
            "description": "person name",
            "id": "48df3a78-2989-5a93-bcfc-c00bbf2626d4",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "person name",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759864159218,
            "version": 1
        },
        "5714b1f5-be77-5d30-94da-ca7f1945e6cd": {
            "created_at": 1759864533114,
            "id": "5714b1f5-be77-5d30-94da-ca7f1945e6cd",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Heather Grace Hewer, also known as Heski in Australia and later Heather Hewer in Denmark, showcased her acting skills by portraying Elizabeth Bennet in a 2003 independent film. She also played Paige Morgan across four films in the 'The Prince & Me' franchise from 2006 to 2010.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759864540332,
            "version": 1
        },
        "5b27b253-0861-567c-a4cd-84f86143a1a1": {
            "created_at": 1759864116781,
            "description": "Birth name of Kam Heskin",
            "id": "5b27b253-0861-567c-a4cd-84f86143a1a1",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "kam erika heskin",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759864159218,
            "version": 1
        },
        "5d7836ab-afef-54c5-8c98-e0d68d4cba2e": {
            "created_at": 1759864153040,
            "id": "5d7836ab-afef-54c5-8c98-e0d68d4cba2e",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin is an accomplished American actress with a career spanning several years.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759864159218,
            "version": 1
        },
        "5f710d9d-8811-5cfb-9175-c5c0533b82ca": {
            "created_at": 1759864290919,
            "description": "film",
            "id": "5f710d9d-8811-5cfb-9175-c5c0533b82ca",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "film",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759864348157,
            "version": 1
        },
        "664d4c41-2b73-5130-9001-35cb8940b2b5": {
            "created_at": 1759863710276,
            "description": "Actress featured in 'The Prince and Me'.",
            "id": "664d4c41-2b73-5130-9001-35cb8940b2b5",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "alberta watson",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759863754879,
            "version": 1
        },
        "703623a6-1dc5-5a33-a19a-44cbd0e6181f": {
            "created_at": 1759863881601,
            "id": "703623a6-1dc5-5a33-a19a-44cbd0e6181f",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The film centers on Paige Morgan, a pre-med student at a college in Wisconsin.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759863888214,
            "version": 1
        },
        "708737b4-7c67-55a0-a9fa-c51e47c5667a": {
            "created_at": 1759863510805,
            "id": "708737b4-7c67-55a0-a9fa-c51e47c5667a",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The movie 'The Prince and Me' follows a determined Irish-American college student named Paige whose plans for a career and marriage are disrupted when she unexpectedly becomes involved with a royal prince, Prince Edward of Wales. The film explores themes of love, duty, and breaking traditional expectations.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759863517064,
            "version": 1
        },
        "777d1f13-44be-59cb-bebf-95fe1b43bc11": {
            "created_at": 1759864290917,
            "description": "Played a character on the NBC daytime soap opera 'Sunset Beach'.",
            "id": "777d1f13-44be-59cb-bebf-95fe1b43bc11",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "caitlin richards deschanel",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759864348157,
            "version": 1
        },
        "78685f7d-ef7e-521b-98fe-e3b90cc6dc74": {
            "chunk_index": 0,
            "chunk_size": 68,
            "contains": [],
            "created_at": 1759864355870,
            "cut_type": "sentence_end",
            "id": "78685f7d-ef7e-521b-98fe-e3b90cc6dc74",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": " Heskin went to play Elizabeth Bennet in the 2003 independent film \"\", and Paige Morgan in the \"The Prince and Me\" film franchise (2006–2010).",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759864540332,
            "version": 1
        },
        "79479bf1-8081-588c-9aed-8d5925d98091": {
            "created_at": 1759864013544,
            "external_metadata": "{}",
            "id": "79479bf1-8081-588c-9aed-8d5925d98091",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_e90368fc3d2373bd3c7bb487f20db2c3",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_e90368fc3d2373bd3c7bb487f20db2c3.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759864159218,
            "version": 1
        },
        "7fe7adc6-5a25-519f-ad0b-c14ecedfe6e6": {
            "created_at": 1759864290917,
            "description": "thing",
            "id": "7fe7adc6-5a25-519f-ad0b-c14ecedfe6e6",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "thing",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759864298332,
            "version": 1
        },
        "8708676d-6bea-578e-94e4-6e1eb607e342": {
            "created_at": 1759863761156,
            "external_metadata": "{}",
            "id": "8708676d-6bea-578e-94e4-6e1eb607e342",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_be7a9849b7da3fe3ac22de8ce398250d",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_be7a9849b7da3fe3ac22de8ce398250d.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759863888214,
            "version": 1
        },
        "87b90780-ba84-50e2-a755-23e6d86cfe4c": {
            "created_at": 1759863710270,
            "description": "A romantic comedy film directed by Martha Coolidge.",
            "id": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "the prince and me",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759863754879,
            "version": 1
        },
        "96d41bf3-11c9-50c5-9094-a27db839e3d7": {
            "created_at": 1759863710275,
            "description": "Actor featured in 'The Prince and Me'.",
            "id": "96d41bf3-11c9-50c5-9094-a27db839e3d7",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "james fox",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759863754879,
            "version": 1
        },
        "a1462b57-6f64-5198-b06c-002de8a0e09d": {
            "created_at": 1759863405476,
            "external_metadata": "{}",
            "id": "a1462b57-6f64-5198-b06c-002de8a0e09d",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_253becda393cc4221094e8eb3cabf879",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_253becda393cc4221094e8eb3cabf879.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759863517064,
            "version": 1
        },
        "a2bfbb88-667a-5ef2-ac65-95ada47283f7": {
            "created_at": 1759864290919,
            "description": "A film from 2001.",
            "id": "a2bfbb88-667a-5ef2-ac65-95ada47283f7",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "planet of the apes",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759864348157,
            "version": 1
        },
        "a900fc95-ce79-55da-b56b-0b0b1fe12da4": {
            "created_at": 1759863710268,
            "description": "creativework",
            "id": "a900fc95-ce79-55da-b56b-0b0b1fe12da4",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "creativework",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759863716738,
            "version": 1
        },
        "acbbcc88-cf50-52fc-97bd-673d1e51ec11": {
            "chunk_index": 0,
            "chunk_size": 79,
            "created_at": 1759863523930,
            "cut_type": "sentence_end",
            "id": "acbbcc88-cf50-52fc-97bd-673d1e51ec11",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me is a 2004 romantic comedy film directed by Martha Coolidge, and starring Julia Stiles, Luke Mably, and Ben Miller, with Miranda Richardson, James Fox, and Alberta Watson.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759863754879,
            "version": 1
        },
        "acf80a29-7aaf-5f5a-87fb-720408e154b6": {
            "created_at": 1759864290919,
            "description": "A film from 2002.",
            "id": "acf80a29-7aaf-5f5a-87fb-720408e154b6",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "catch me if you can",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759864348157,
            "version": 1
        },
        "b044d8c8-8604-5421-a4f5-48d3378641d9": {
            "created_at": 1759864340317,
            "id": "b044d8c8-8604-5421-a4f5-48d3378641d9",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The actress began her career on 'Sunset Beach' as Caitlin Richards Deschanel (1998–1999) and later appeared in 'Planet of the Apes' (2001) and 'Catch Me If You Can' (2002).",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759864348157,
            "version": 1
        },
        "b1ce3cf9-5e41-5d08-93a6-830b1a96ef4a": {
            "created_at": 1759863894874,
            "external_metadata": "{}",
            "id": "b1ce3cf9-5e41-5d08-93a6-830b1a96ef4a",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_c848f59aad5b304add1773efba5b0762",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_c848f59aad5b304add1773efba5b0762.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759864007223,
            "version": 1
        },
        "ba6437b2-8c75-5164-aed3-c9e53f6f0265": {
            "created_at": 1759864354729,
            "external_metadata": "{}",
            "id": "ba6437b2-8c75-5164-aed3-c9e53f6f0265",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_986e4ef18b400a6074fc04116fc4f4bd",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_986e4ef18b400a6074fc04116fc4f4bd.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759864540332,
            "version": 1
        },
        "bfae514a-cfed-5429-8295-a1db7a7e2241": {
            "created_at": 1759864116780,
            "description": "American actress",
            "id": "bfae514a-cfed-5429-8295-a1db7a7e2241",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "kam heskin",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759864159218,
            "version": 1
        },
        "c11b5618-a778-56c3-84d2-0c3e0542641a": {
            "created_at": 1759864290918,
            "description": "television show",
            "id": "c11b5618-a778-56c3-84d2-0c3e0542641a",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "television show",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759864348157,
            "version": 1
        },
        "d072ba0f-e1a9-58bf-9974-e1802adc8134": {
            "created_at": 1759864290917,
            "description": "person",
            "id": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "person",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759864348157,
            "version": 1
        },
        "d48a7618-4ea5-52f2-be85-68ba46d0789e": {
            "chunk_index": 0,
            "chunk_size": 101,
            "created_at": 1759864166806,
            "cut_type": "sentence_end",
            "id": "d48a7618-4ea5-52f2-be85-68ba46d0789e",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": " She began her career playing Caitlin Richards Deschanel on the NBC daytime soap opera \"Sunset Beach\" (1998–1999), before appearing in films \"Planet of the Apes\" (2001 and \"Catch Me If You Can\" (2002).",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759864348157,
            "version": 1
        },
        "d61d99ac-b291-5666-9748-3e80e1c8b56a": {
            "created_at": 1759864116780,
            "description": "date",
            "id": "d61d99ac-b291-5666-9748-3e80e1c8b56a",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "date",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759864159218,
            "version": 1
        },
        "d8afed96-bf61-534f-b3f8-5ab66dbfd7e4": {
            "created_at": 1759863522741,
            "external_metadata": "{}",
            "id": "d8afed96-bf61-534f-b3f8-5ab66dbfd7e4",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_0d8bce0ea5edd9bf132de26723b43b94",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_0d8bce0ea5edd9bf132de26723b43b94.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759863754879,
            "version": 1
        },
        "ef8e4b65-4096-5f16-b41b-7fc58935f537": {
            "created_at": 1759864290919,
            "description": "An NBC daytime soap opera.",
            "id": "ef8e4b65-4096-5f16-b41b-7fc58935f537",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "sunset beach",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759864348157,
            "version": 1
        },
        "f1c7b09c-457a-580d-8991-291e03750755": {
            "created_at": 1759863747195,
            "id": "f1c7b09c-457a-580d-8991-291e03750755",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me is a 2004 romantic comedy film directed by Martha Coolidge.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759863754879,
            "version": 1
        },
        "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0": {
            "created_at": 1759863710271,
            "description": "Actress starring in 'The Prince and Me'.",
            "id": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "julia stiles",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759863754879,
            "version": 1
        },
        "f7210df6-380d-597c-a594-72ee0854a798": {
            "created_at": 1759863710271,
            "description": "Actor starring in 'The Prince and Me'.",
            "id": "f7210df6-380d-597c-a594-72ee0854a798",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "luke mably",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759863754879,
            "version": 1
        },
        "f84966cf-217c-5f70-83d0-21ce5d08be39": {
            "chunk_index": 0,
            "chunk_size": 5,
            "created_at": 1759863896108,
            "cut_type": "sentence_cut",
            "id": "f84966cf-217c-5f70-83d0-21ce5d08be39",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759864007223,
            "version": 1
        },
        "faf5923c-ce35-5f90-96cf-259e3c074f8f": {
            "created_at": 1759864116780,
            "description": "",
            "id": "faf5923c-ce35-5f90-96cf-259e3c074f8f",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "may 8, 1973",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759864159218,
            "version": 1
        },
        "fee17662-f962-5bba-ab3c-1f889a7a6b40": {
            "created_at": 1759863710268,
            "description": "movie",
            "id": "fee17662-f962-5bba-ab3c-1f889a7a6b40",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "movie",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759863754879,
            "version": 1
        }
    },
    "edges": 
    {
        "edge1": {
            "label": "is_part_of",
            "source": "43e98278-8388-5c90-ab26-e59b77c0a8d1",
            "target": "a1462b57-6f64-5198-b06c-002de8a0e09d"
        },
        "edge10": {
            "label": "contains",
            "source": "acbbcc88-cf50-52fc-97bd-673d1e51ec11",
            "target": "f7210df6-380d-597c-a594-72ee0854a798"
        },
        "edge11": {
            "label": "is_a",
            "source": "f7210df6-380d-597c-a594-72ee0854a798",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge12": {
            "label": "contains",
            "source": "acbbcc88-cf50-52fc-97bd-673d1e51ec11",
            "target": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc"
        },
        "edge13": {
            "label": "is_a",
            "source": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge14": {
            "label": "contains",
            "source": "acbbcc88-cf50-52fc-97bd-673d1e51ec11",
            "target": "48355aef-4600-5836-a677-65d05d620689"
        },
        "edge15": {
            "label": "is_a",
            "source": "48355aef-4600-5836-a677-65d05d620689",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge16": {
            "label": "contains",
            "source": "acbbcc88-cf50-52fc-97bd-673d1e51ec11",
            "target": "96d41bf3-11c9-50c5-9094-a27db839e3d7"
        },
        "edge17": {
            "label": "is_a",
            "source": "96d41bf3-11c9-50c5-9094-a27db839e3d7",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge18": {
            "label": "contains",
            "source": "acbbcc88-cf50-52fc-97bd-673d1e51ec11",
            "target": "664d4c41-2b73-5130-9001-35cb8940b2b5"
        },
        "edge19": {
            "label": "is_a",
            "source": "664d4c41-2b73-5130-9001-35cb8940b2b5",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge2": {
            "label": "made_from",
            "source": "708737b4-7c67-55a0-a9fa-c51e47c5667a",
            "target": "43e98278-8388-5c90-ab26-e59b77c0a8d1"
        },
        "edge20": {
            "label": "directed_by",
            "source": "1c877e38-afdb-5af9-bfa1-c14235256bbe",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge21": {
            "label": "acted_in",
            "source": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge22": {
            "label": "acted_in",
            "source": "f7210df6-380d-597c-a594-72ee0854a798",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge23": {
            "label": "acted_in",
            "source": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge24": {
            "label": "featured_in",
            "source": "48355aef-4600-5836-a677-65d05d620689",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge25": {
            "label": "featured_in",
            "source": "96d41bf3-11c9-50c5-9094-a27db839e3d7",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge26": {
            "label": "featured_in",
            "source": "664d4c41-2b73-5130-9001-35cb8940b2b5",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge27": {
            "label": "is_a",
            "source": "fee17662-f962-5bba-ab3c-1f889a7a6b40",
            "target": "a900fc95-ce79-55da-b56b-0b0b1fe12da4"
        },
        "edge28": {
            "label": "is_a",
            "source": "a900fc95-ce79-55da-b56b-0b0b1fe12da4",
            "target": "7fe7adc6-5a25-519f-ad0b-c14ecedfe6e6"
        },
        "edge29": {
            "label": "is_a",
            "source": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
            "target": "7fe7adc6-5a25-519f-ad0b-c14ecedfe6e6"
        },
        "edge3": {
            "label": "is_part_of",
            "source": "acbbcc88-cf50-52fc-97bd-673d1e51ec11",
            "target": "d8afed96-bf61-534f-b3f8-5ab66dbfd7e4"
        },
        "edge30": {
            "label": "made_from",
            "source": "f1c7b09c-457a-580d-8991-291e03750755",
            "target": "acbbcc88-cf50-52fc-97bd-673d1e51ec11"
        },
        "edge31": {
            "label": "is_part_of",
            "source": "00ba6221-07c8-5f26-bae3-c0e79f2ff783",
            "target": "8708676d-6bea-578e-94e4-6e1eb607e342"
        },
        "edge32": {
            "label": "made_from",
            "source": "703623a6-1dc5-5a33-a19a-44cbd0e6181f",
            "target": "00ba6221-07c8-5f26-bae3-c0e79f2ff783"
        },
        "edge33": {
            "label": "is_part_of",
            "source": "f84966cf-217c-5f70-83d0-21ce5d08be39",
            "target": "b1ce3cf9-5e41-5d08-93a6-830b1a96ef4a"
        },
        "edge34": {
            "label": "contains",
            "source": "f84966cf-217c-5f70-83d0-21ce5d08be39",
            "target": "bfae514a-cfed-5429-8295-a1db7a7e2241"
        },
        "edge35": {
            "label": "is_a",
            "source": "bfae514a-cfed-5429-8295-a1db7a7e2241",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge36": {
            "label": "made_from",
            "source": "0f7c3e65-da98-57aa-9793-3919242b7edb",
            "target": "f84966cf-217c-5f70-83d0-21ce5d08be39"
        },
        "edge37": {
            "label": "is_part_of",
            "source": "44d222d6-0a45-5a61-a030-dd082df76979",
            "target": "79479bf1-8081-588c-9aed-8d5925d98091"
        },
        "edge38": {
            "label": "contains",
            "source": "44d222d6-0a45-5a61-a030-dd082df76979",
            "target": "bfae514a-cfed-5429-8295-a1db7a7e2241"
        },
        "edge39": {
            "label": "contains",
            "source": "44d222d6-0a45-5a61-a030-dd082df76979",
            "target": "faf5923c-ce35-5f90-96cf-259e3c074f8f"
        },
        "edge4": {
            "label": "contains",
            "source": "acbbcc88-cf50-52fc-97bd-673d1e51ec11",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge40": {
            "label": "is_a",
            "source": "faf5923c-ce35-5f90-96cf-259e3c074f8f",
            "target": "d61d99ac-b291-5666-9748-3e80e1c8b56a"
        },
        "edge41": {
            "label": "contains",
            "source": "44d222d6-0a45-5a61-a030-dd082df76979",
            "target": "5b27b253-0861-567c-a4cd-84f86143a1a1"
        },
        "edge42": {
            "label": "is_a",
            "source": "5b27b253-0861-567c-a4cd-84f86143a1a1",
            "target": "48df3a78-2989-5a93-bcfc-c00bbf2626d4"
        },
        "edge43": {
            "label": "known_as",
            "source": "bfae514a-cfed-5429-8295-a1db7a7e2241",
            "target": "5b27b253-0861-567c-a4cd-84f86143a1a1"
        },
        "edge44": {
            "label": "born_on",
            "source": "bfae514a-cfed-5429-8295-a1db7a7e2241",
            "target": "faf5923c-ce35-5f90-96cf-259e3c074f8f"
        },
        "edge45": {
            "label": "made_from",
            "source": "5d7836ab-afef-54c5-8c98-e0d68d4cba2e",
            "target": "44d222d6-0a45-5a61-a030-dd082df76979"
        },
        "edge46": {
            "label": "is_part_of",
            "source": "d48a7618-4ea5-52f2-be85-68ba46d0789e",
            "target": "27a88ae9-bd27-5e0b-a5c4-064ca1b72ee2"
        },
        "edge47": {
            "label": "contains",
            "source": "d48a7618-4ea5-52f2-be85-68ba46d0789e",
            "target": "777d1f13-44be-59cb-bebf-95fe1b43bc11"
        },
        "edge48": {
            "label": "is_a",
            "source": "777d1f13-44be-59cb-bebf-95fe1b43bc11",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge49": {
            "label": "contains",
            "source": "d48a7618-4ea5-52f2-be85-68ba46d0789e",
            "target": "ef8e4b65-4096-5f16-b41b-7fc58935f537"
        },
        "edge5": {
            "label": "is_a",
            "source": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "target": "fee17662-f962-5bba-ab3c-1f889a7a6b40"
        },
        "edge50": {
            "label": "is_a",
            "source": "ef8e4b65-4096-5f16-b41b-7fc58935f537",
            "target": "c11b5618-a778-56c3-84d2-0c3e0542641a"
        },
        "edge51": {
            "label": "contains",
            "source": "d48a7618-4ea5-52f2-be85-68ba46d0789e",
            "target": "a2bfbb88-667a-5ef2-ac65-95ada47283f7"
        },
        "edge52": {
            "label": "is_a",
            "source": "a2bfbb88-667a-5ef2-ac65-95ada47283f7",
            "target": "5f710d9d-8811-5cfb-9175-c5c0533b82ca"
        },
        "edge53": {
            "label": "contains",
            "source": "d48a7618-4ea5-52f2-be85-68ba46d0789e",
            "target": "acf80a29-7aaf-5f5a-87fb-720408e154b6"
        },
        "edge54": {
            "label": "is_a",
            "source": "acf80a29-7aaf-5f5a-87fb-720408e154b6",
            "target": "5f710d9d-8811-5cfb-9175-c5c0533b82ca"
        },
        "edge55": {
            "label": "acted_in",
            "source": "777d1f13-44be-59cb-bebf-95fe1b43bc11",
            "target": "ef8e4b65-4096-5f16-b41b-7fc58935f537"
        },
        "edge56": {
            "label": "appeared_in",
            "source": "777d1f13-44be-59cb-bebf-95fe1b43bc11",
            "target": "a2bfbb88-667a-5ef2-ac65-95ada47283f7"
        },
        "edge57": {
            "label": "appeared_in",
            "source": "777d1f13-44be-59cb-bebf-95fe1b43bc11",
            "target": "acf80a29-7aaf-5f5a-87fb-720408e154b6"
        },
        "edge58": {
            "label": "made_from",
            "source": "b044d8c8-8604-5421-a4f5-48d3378641d9",
            "target": "d48a7618-4ea5-52f2-be85-68ba46d0789e"
        },
        "edge59": {
            "label": "is_part_of",
            "source": "78685f7d-ef7e-521b-98fe-e3b90cc6dc74",
            "target": "ba6437b2-8c75-5164-aed3-c9e53f6f0265"
        },
        "edge6": {
            "label": "contains",
            "source": "acbbcc88-cf50-52fc-97bd-673d1e51ec11",
            "target": "1c877e38-afdb-5af9-bfa1-c14235256bbe"
        },
        "edge60": {
            "label": "made_from",
            "source": "5714b1f5-be77-5d30-94da-ca7f1945e6cd",
            "target": "78685f7d-ef7e-521b-98fe-e3b90cc6dc74"
        },
        "edge7": {
            "label": "is_a",
            "source": "1c877e38-afdb-5af9-bfa1-c14235256bbe",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge8": {
            "label": "contains",
            "source": "acbbcc88-cf50-52fc-97bd-673d1e51ec11",
            "target": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0"
        },
        "edge9": {
            "label": "is_a",
            "source": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        }
    }
}

FIXED_RESULT4 = {
    "final_answer": "In the 2004 film 'The Prince and Me,' Kam Heskin plays Paige Morgan. The director of the film is Martha Coolidge, whose first name has four letters between the 'M' and the 'a': r, t, h.",
    "nodes": 
    {
        "06e65008-a5a0-54ab-8399-5d02e1c50294": {
            "created_at": 1759867720649,
            "description": "administrativearea",
            "id": "06e65008-a5a0-54ab-8399-5d02e1c50294",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "administrativearea",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759867726469,
            "version": 1
        },
        "07e1512b-5e03-5133-a19b-1f45f2e64c0f": {
            "created_at": 1759866723840,
            "description": "tv show",
            "id": "07e1512b-5e03-5133-a19b-1f45f2e64c0f",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "tv show",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759866792105,
            "version": 1
        },
        "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc": {
            "created_at": 1759866089135,
            "description": "Acted in The Prince and Me",
            "id": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "ben miller",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866135246,
            "version": 1
        },
        "0e7afef2-5b5f-5c43-87a9-c61e38700ffb": {
            "chunk_index": 0,
            "chunk_size": 79,
            "created_at": 1759865901386,
            "cut_type": "sentence_end",
            "id": "0e7afef2-5b5f-5c43-87a9-c61e38700ffb",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me is a 2004 romantic comedy film directed by Martha Coolidge, and starring Julia Stiles, Luke Mably, and Ben Miller, with Miranda Richardson, James Fox, and Alberta Watson.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759866135246,
            "version": 1
        },
        "0fd1eeaa-69e9-55bc-9d03-8e234a8c95ae": {
            "created_at": 1759867303595,
            "id": "0fd1eeaa-69e9-55bc-9d03-8e234a8c95ae",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me is directed by Clare Kilner.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759867308502,
            "version": 1
        },
        "13b2974d-0214-5cc7-b5e7-5ac4bcbb6e49": {
            "chunk_index": 0,
            "chunk_size": 7,
            "created_at": 1759865666985,
            "cut_type": "sentence_cut",
            "id": "13b2974d-0214-5cc7-b5e7-5ac4bcbb6e49",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759865895804,
            "version": 1
        },
        "1612ea96-8870-5cf0-8680-63787271d6e0": {
            "created_at": 1759867589510,
            "external_metadata": "{}",
            "id": "1612ea96-8870-5cf0-8680-63787271d6e0",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_a87ff679a2f3e71d9181a67b7542122c",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_a87ff679a2f3e71d9181a67b7542122c.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759867757892,
            "version": 1
        },
        "1c877e38-afdb-5af9-bfa1-c14235256bbe": {
            "created_at": 1759867528405,
            "description": "American director and producer",
            "id": "1c877e38-afdb-5af9-bfa1-c14235256bbe",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "martha coolidge",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759867581439,
            "version": 1
        },
        "1d32ad5d-f120-5b70-bafb-1e51e41f3e90": {
            "created_at": 1759866521794,
            "description": "Birth date of Kam Erika Heskin",
            "id": "1d32ad5d-f120-5b70-bafb-1e51e41f3e90",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "may 8, 1973",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866565151,
            "version": 1
        },
        "1f952b2e-6fa5-5842-8d7a-048da390df9b": {
            "created_at": 1759867720650,
            "description": "The date on which John F. Kennedy was assassinated, November 22, 1963.",
            "id": "1f952b2e-6fa5-5842-8d7a-048da390df9b",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "assassination date",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759867757892,
            "version": 1
        },
        "21d19d74-b14b-5c0a-9272-20904a2f8c73": {
            "created_at": 1759866243231,
            "description": "a prince posing as a normal college student",
            "id": "21d19d74-b14b-5c0a-9272-20904a2f8c73",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "prince",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866292496,
            "version": 1
        },
        "232d7e4f-a348-5895-8e41-dec5312ff095": {
            "created_at": 1759866126605,
            "id": "232d7e4f-a348-5895-8e41-dec5312ff095",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me is a romantic comedy film from 2004.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759866135246,
            "version": 1
        },
        "247e6b40-9b47-550a-83e1-bc4fdb1055b6": {
            "created_at": 1759866570717,
            "external_metadata": "{}",
            "id": "247e6b40-9b47-550a-83e1-bc4fdb1055b6",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_01a827d5156ebe7bf6384321dae464f9",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_01a827d5156ebe7bf6384321dae464f9.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759866792105,
            "version": 1
        },
        "26bd435e-a9d0-545e-af08-1961fa600f55": {
            "created_at": 1759865854317,
            "description": "A BBC radio station where Prince Edward VIII recorded a tribute to Wallis Simpson.",
            "id": "26bd435e-a9d0-545e-af08-1961fa600f55",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "bbc radio 2",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759865895804,
            "version": 1
        },
        "33123e17-ef57-5eab-821b-983fdf32b0c2": {
            "created_at": 1759867002870,
            "external_metadata": "{}",
            "id": "33123e17-ef57-5eab-821b-983fdf32b0c2",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_a1a220f8f21dbd8094bc6dbd0e7f22c8",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_a1a220f8f21dbd8094bc6dbd0e7f22c8.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759867174249,
            "version": 1
        },
        "35055cab-a39f-58fa-89ec-8d385fc80f47": {
            "chunk_index": 0,
            "chunk_size": 101,
            "created_at": 1759866571531,
            "cut_type": "sentence_end",
            "id": "35055cab-a39f-58fa-89ec-8d385fc80f47",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": " She began her career playing Caitlin Richards Deschanel on the NBC daytime soap opera \"Sunset Beach\" (1998–1999), before appearing in films \"Planet of the Apes\" (2001 and \"Catch Me If You Can\" (2002).",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759866792105,
            "version": 1
        },
        "36f04799-e348-5658-8927-3779ac6171a1": {
            "created_at": 1759867189106,
            "external_metadata": "{}",
            "id": "36f04799-e348-5658-8927-3779ac6171a1",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_50540eb05e14b27c751b5c2bcb248338",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_50540eb05e14b27c751b5c2bcb248338.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759867308502,
            "version": 1
        },
        "3e1fc0b7-0586-5d76-a13b-98eed72e6877": {
            "created_at": 1759866286000,
            "id": "3e1fc0b7-0586-5d76-a13b-98eed72e6877",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The film centers on Paige Morgan, a pre-med student at a Wisconsin college who is courted by a prince disguising himself as an ordinary student.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759866292496,
            "version": 1
        },
        "4130f70e-5e5b-581e-91f1-d60174bd7c94": {
            "created_at": 1759866141036,
            "external_metadata": "{}",
            "id": "4130f70e-5e5b-581e-91f1-d60174bd7c94",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_be7a9849b7da3fe3ac22de8ce398250d",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_be7a9849b7da3fe3ac22de8ce398250d.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759866292496,
            "version": 1
        },
        "48355aef-4600-5836-a677-65d05d620689": {
            "created_at": 1759866089135,
            "description": "Cast member of The Prince and Me",
            "id": "48355aef-4600-5836-a677-65d05d620689",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "miranda richardson",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866135246,
            "version": 1
        },
        "4e4e97bd-4a6e-539b-9648-95fdedc7ee2b": {
            "chunk_index": 0,
            "chunk_size": 5,
            "created_at": 1759866299834,
            "cut_type": "sentence_cut",
            "id": "4e4e97bd-4a6e-539b-9648-95fdedc7ee2b",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759866419888,
            "version": 1
        },
        "4ff7696e-9e02-5a7e-826a-8ddd833bad18": {
            "created_at": 1759865890283,
            "id": "4ff7696e-9e02-5a7e-826a-8ddd833bad18",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759865895804,
            "version": 1
        },
        "5b27b253-0861-567c-a4cd-84f86143a1a1": {
            "created_at": 1759866521793,
            "description": "American actress",
            "id": "5b27b253-0861-567c-a4cd-84f86143a1a1",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "kam heskin",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866565151,
            "version": 1
        },
        "5f710d9d-8811-5cfb-9175-c5c0533b82ca": {
            "created_at": 1759866723841,
            "description": "film",
            "id": "5f710d9d-8811-5cfb-9175-c5c0533b82ca",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "film",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759866792105,
            "version": 1
        },
        "5fde067d-2a61-579b-a775-9bf52b23053c": {
            "created_at": 1759866298996,
            "external_metadata": "{}",
            "id": "5fde067d-2a61-579b-a775-9bf52b23053c",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_c848f59aad5b304add1773efba5b0762",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_c848f59aad5b304add1773efba5b0762.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759866419888,
            "version": 1
        },
        "60400025-6197-59e8-a985-b020912a6521": {
            "chunk_index": 0,
            "chunk_size": 16,
            "contains": [],
            "created_at": 1759867190208,
            "cut_type": "sentence_end",
            "id": "60400025-6197-59e8-a985-b020912a6521",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The Prince and Me is directed by who?",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759867308502,
            "version": 1
        },
        "66127932-b89f-5cac-bfb3-8132b4119cbd": {
            "created_at": 1759866243230,
            "description": "a pre-med college student",
            "id": "66127932-b89f-5cac-bfb3-8132b4119cbd",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "paige morgan",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866292496,
            "version": 1
        },
        "664d4c41-2b73-5130-9001-35cb8940b2b5": {
            "created_at": 1759866089135,
            "description": "Acted in The Prince and Me",
            "id": "664d4c41-2b73-5130-9001-35cb8940b2b5",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "alberta watson",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866135246,
            "version": 1
        },
        "66e0cbd6-3db5-5178-af77-507bfbab152d": {
            "created_at": 1759866559401,
            "id": "66e0cbd6-3db5-5178-af77-507bfbab152d",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "American actress biography",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759866565151,
            "version": 1
        },
        "6848eb4b-e3f5-5c5d-b68b-91a6f3ecc48c": {
            "created_at": 1759866798065,
            "external_metadata": "{}",
            "id": "6848eb4b-e3f5-5c5d-b68b-91a6f3ecc48c",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_986e4ef18b400a6074fc04116fc4f4bd",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_986e4ef18b400a6074fc04116fc4f4bd.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759866993605,
            "version": 1
        },
        "6fb9b7b8-156a-5559-bd7b-f0bd81bca160": {
            "created_at": 1759866723840,
            "description": "An NBC daytime soap opera where Caitlin Richards Deschanel played a character.",
            "id": "6fb9b7b8-156a-5559-bd7b-f0bd81bca160",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "sunset beach",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866792105,
            "version": 1
        },
        "72a5d391-5a58-52f2-8058-520d3a5bd2e4": {
            "created_at": 1759867720649,
            "description": "A country in North America that is a federal republic composed of 50 states.",
            "id": "72a5d391-5a58-52f2-8058-520d3a5bd2e4",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "united states of america",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759867757892,
            "version": 1
        },
        "76b73d93-69a8-539b-b220-20ad39f026fd": {
            "created_at": 1759865666108,
            "external_metadata": "{}",
            "id": "76b73d93-69a8-539b-b220-20ad39f026fd",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_253becda393cc4221094e8eb3cabf879",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_253becda393cc4221094e8eb3cabf879.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759865895804,
            "version": 1
        },
        "76bd6a74-912c-546e-bd5b-d38273cdc650": {
            "chunk_index": 0,
            "chunk_size": 4,
            "created_at": 1759867315360,
            "cut_type": "sentence_cut",
            "id": "76bd6a74-912c-546e-bd5b-d38273cdc650",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Martha Coolidge",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759867438874,
            "version": 1
        },
        "777d1f13-44be-59cb-bebf-95fe1b43bc11": {
            "created_at": 1759866723840,
            "description": "Actress who began her career on the soap opera 'Sunset Beach'.",
            "id": "777d1f13-44be-59cb-bebf-95fe1b43bc11",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "caitlin richards deschanel",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866792105,
            "version": 1
        },
        "7fe7adc6-5a25-519f-ad0b-c14ecedfe6e6": {
            "created_at": 1759867720646,
            "description": "thing",
            "id": "7fe7adc6-5a25-519f-ad0b-c14ecedfe6e6",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "thing",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759867726469,
            "version": 1
        },
        "87b90780-ba84-50e2-a755-23e6d86cfe4c": {
            "created_at": 1759866089133,
            "description": "A 2004 romantic comedy film directed by Martha Coolidge, starring Julia Stiles, Luke Mably, Ben Miller, Miranda Richardson, James Fox, and Alberta Watson.",
            "id": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "the prince and me",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866135246,
            "version": 1
        },
        "8cfe8577-7e46-5d01-9fac-128e9ec5d969": {
            "chunk_index": 0,
            "chunk_size": 68,
            "contains": [],
            "created_at": 1759866798963,
            "cut_type": "sentence_end",
            "id": "8cfe8577-7e46-5d01-9fac-128e9ec5d969",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": " Heskin went to play Elizabeth Bennet in the 2003 independent film \"\", and Paige Morgan in the \"The Prince and Me\" film franchise (2006–2010).",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759866993605,
            "version": 1
        },
        "90c54eb4-362b-5c0c-9331-d232b7711675": {
            "chunk_index": 0,
            "chunk_size": 56,
            "created_at": 1759866141879,
            "cut_type": "sentence_end",
            "id": "90c54eb4-362b-5c0c-9331-d232b7711675",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": " The film focuses on Paige Morgan, a pre-med college student in Wisconsin, who is pursued by a prince posing as a normal college student.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759866292496,
            "version": 1
        },
        "912b273c-683d-53ea-8ffe-aadef0b84237": {
            "created_at": 1759866243231,
            "description": "educational institution",
            "id": "912b273c-683d-53ea-8ffe-aadef0b84237",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "educational institution",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759866292496,
            "version": 1
        },
        "9249c2a3-2ba6-55d6-b2e6-3917982c2ce4": {
            "created_at": 1759866243231,
            "description": "the college in Wisconsin where Paige studies pre-med",
            "id": "9249c2a3-2ba6-55d6-b2e6-3917982c2ce4",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "wisconsin college",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866292496,
            "version": 1
        },
        "96d41bf3-11c9-50c5-9094-a27db839e3d7": {
            "created_at": 1759866089135,
            "description": "Cast member of The Prince and Me",
            "id": "96d41bf3-11c9-50c5-9094-a27db839e3d7",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "james fox",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866135246,
            "version": 1
        },
        "9702e91d-6622-5499-9ecd-a067b77d1a17": {
            "created_at": 1759866414436,
            "id": "9702e91d-6622-5499-9ecd-a067b77d1a17",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin is a fictional character from Marvel Comics.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759866419888,
            "version": 1
        },
        "982ac8a9-4a93-598c-a2dc-18af781b6347": {
            "created_at": 1759867720647,
            "description": "39th President of the United States, served from January 20, 1961, until his assassination on November 22, 1963.",
            "id": "982ac8a9-4a93-598c-a2dc-18af781b6347",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "john f. kennedy",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759867757892,
            "version": 1
        },
        "9a549ea8-90bd-5e0c-8c89-a496a570a084": {
            "created_at": 1759866987333,
            "id": "9a549ea8-90bd-5e0c-8c89-a496a570a084",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Heskin portrayed Elizabeth Bennet in a 2003 independent film and played Paige Morgan in 'The Prince and Me' series from 2006 to 2010.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759866993605,
            "version": 1
        },
        "9bd785c8-5371-520c-a239-39de82264b0f": {
            "created_at": 1759867720649,
            "description": "country",
            "id": "9bd785c8-5371-520c-a239-39de82264b0f",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "country",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759867757892,
            "version": 1
        },
        "a2bfbb88-667a-5ef2-ac65-95ada47283f7": {
            "created_at": 1759866723841,
            "description": "A film in which Caitlin Richards Deschanel appeared, released in 2001.",
            "id": "a2bfbb88-667a-5ef2-ac65-95ada47283f7",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "planet of the apes",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866792105,
            "version": 1
        },
        "a3be1b91-8617-51a1-ac6c-33c89e7564cb": {
            "chunk_index": 0,
            "chunk_size": 25,
            "contains": [],
            "created_at": 1759867003666,
            "cut_type": "sentence_end",
            "id": "a3be1b91-8617-51a1-ac6c-33c89e7564cb",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin plays Paige Morgan in which 2004 film?",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759867174249,
            "version": 1
        },
        "a494b807-21e0-5bc2-9d7d-5a206d3b6c8c": {
            "chunk_index": 0,
            "chunk_size": 37,
            "created_at": 1759867452652,
            "cut_type": "sentence_end",
            "id": "a494b807-21e0-5bc2-9d7d-5a206d3b6c8c",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "How many letters are there between the first and last letters of the first name of Martha Coolidge?",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759867581439,
            "version": 1
        },
        "a4e9d9a8-7bc4-57f3-8135-0220c8be2f4b": {
            "created_at": 1759866782426,
            "id": "a4e9d9a8-7bc4-57f3-8135-0220c8be2f4b",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "The actress started her career on the soap opera 'Sunset Beach' as Caitlin Richards Deschanel and later appeared in films including 'Planet of the Apes' (2001) and 'Catch Me If You Can' (2002).",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759866792105,
            "version": 1
        },
        "a66adf89-e844-5272-a946-ce9ccf161b6b": {
            "chunk_index": 0,
            "chunk_size": 41,
            "created_at": 1759866426635,
            "cut_type": "sentence_end",
            "id": "a66adf89-e844-5272-a946-ce9ccf161b6b",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin (born Kam Erika Heskin on May 8, 1973) is an American actress.",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759866565151,
            "version": 1
        },
        "a900fc95-ce79-55da-b56b-0b0b1fe12da4": {
            "created_at": 1759865854318,
            "description": "creativework",
            "id": "a900fc95-ce79-55da-b56b-0b0b1fe12da4",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "creativework",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759865860549,
            "version": 1
        },
        "a9ca3cc1-b6ba-5497-bea8-aeffa3a322ab": {
            "created_at": 1759867314546,
            "external_metadata": "{}",
            "id": "a9ca3cc1-b6ba-5497-bea8-aeffa3a322ab",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_e2ac58d8ccd36d90a192d6e7ca162a44",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_e2ac58d8ccd36d90a192d6e7ca162a44.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759867438874,
            "version": 1
        },
        "abadc643-fea0-5250-ab09-765309cbcc2f": {
            "created_at": 1759865854314,
            "description": "The family of British monarchs.",
            "id": "abadc643-fea0-5250-ab09-765309cbcc2f",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "british royal family",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759865895804,
            "version": 1
        },
        "acf80a29-7aaf-5f5a-87fb-720408e154b6": {
            "created_at": 1759866723841,
            "description": "A film in which Caitlin Richards Deschanel appeared, released in 2002.",
            "id": "acf80a29-7aaf-5f5a-87fb-720408e154b6",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "catch me if you can",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866792105,
            "version": 1
        },
        "b1c8236e-7c6c-56a4-985a-a609809cab3f": {
            "created_at": 1759865854317,
            "description": "media outfit",
            "id": "b1c8236e-7c6c-56a4-985a-a609809cab3f",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "media outfit",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759865895804,
            "version": 1
        },
        "b1d80755-1dd1-56e7-a372-486d60958d02": {
            "created_at": 1759865854307,
            "description": "The Prince of Wales and heir to the throne, referred by some as ‘Wallis’s man’.",
            "id": "b1d80755-1dd1-56e7-a372-486d60958d02",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "prince edward viii",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759865895804,
            "version": 1
        },
        "b5353ef8-9d5c-55c4-8049-41b9d8108760": {
            "created_at": 1759865854307,
            "description": "An American divorcée involved with Prince Edward VIII, causing a constitutional crisis when he abdicated the throne for her.",
            "id": "b5353ef8-9d5c-55c4-8049-41b9d8108760",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "wallis simpson",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759865895804,
            "version": 1
        },
        "b661854d-2f9b-5b09-93f9-77be0be05db9": {
            "created_at": 1759865854306,
            "description": "A recent college graduate.",
            "id": "b661854d-2f9b-5b09-93f9-77be0be05db9",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "rachel",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759865895804,
            "version": 1
        },
        "b711a2f8-bdc5-5f87-832a-25022b1e53f4": {
            "created_at": 1759867752250,
            "id": "b711a2f8-bdc5-5f87-832a-25022b1e53f4",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Section on class label description",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759867757892,
            "version": 1
        },
        "bfae514a-cfed-5429-8295-a1db7a7e2241": {
            "created_at": 1759866372237,
            "description": "There is no additional context provided about Kam Heskin, leaving room for further information if available.",
            "id": "bfae514a-cfed-5429-8295-a1db7a7e2241",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "kam heskin",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866419888,
            "version": 1
        },
        "c404dd9b-4545-5a30-81e0-cd700f696e21": {
            "created_at": 1759867575024,
            "id": "c404dd9b-4545-5a30-81e0-cd700f696e21",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Martha Coolidge's first name 'Martha' has 4 letters between the first ('M') and last letter ('a').",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759867581439,
            "version": 1
        },
        "d072ba0f-e1a9-58bf-9974-e1802adc8134": {
            "created_at": 1759867720646,
            "description": "person",
            "id": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "person",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759867757892,
            "version": 1
        },
        "d3d7b6b4-9b0d-52e8-9e09-a9e9cf4b5a4d": {
            "created_at": 1759865854313,
            "description": "organization",
            "id": "d3d7b6b4-9b0d-52e8-9e09-a9e9cf4b5a4d",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "organization",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759865895804,
            "version": 1
        },
        "d61d99ac-b291-5666-9748-3e80e1c8b56a": {
            "created_at": 1759867720650,
            "description": "date",
            "id": "d61d99ac-b291-5666-9748-3e80e1c8b56a",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "date",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759867757892,
            "version": 1
        },
        "dcc891ef-1e18-5b32-9758-dd822d32f133": {
            "created_at": 1759866426039,
            "external_metadata": "{}",
            "id": "dcc891ef-1e18-5b32-9758-dd822d32f133",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_e90368fc3d2373bd3c7bb487f20db2c3",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_e90368fc3d2373bd3c7bb487f20db2c3.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759866565151,
            "version": 1
        },
        "df23bf40-916e-551c-bd98-9d7ada0706d9": {
            "created_at": 1759867168724,
            "id": "df23bf40-916e-551c-bd98-9d7ada0706d9",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Kam Heskin plays Paige Morgan in 'White Chicks'.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759867174249,
            "version": 1
        },
        "e2011dee-b9d7-53bc-ae22-bba4ca2fe09b": {
            "created_at": 1759867433594,
            "id": "e2011dee-b9d7-53bc-ae22-bba4ca2fe09b",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "Martha Coolidge is an esteemed American film director, screenwriter, and producer.",
            "topological_rank": 0,
            "type": "TextSummary",
            "updated_at": 1759867438874,
            "version": 1
        },
        "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0": {
            "created_at": 1759866089134,
            "description": "Acted in The Prince and Me",
            "id": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "julia stiles",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866135246,
            "version": 1
        },
        "f585f8e0-ef96-53c5-be3f-72cba6465d42": {
            "created_at": 1759865900495,
            "external_metadata": "{}",
            "id": "f585f8e0-ef96-53c5-be3f-72cba6465d42",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_0d8bce0ea5edd9bf132de26723b43b94",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_0d8bce0ea5edd9bf132de26723b43b94.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759866135246,
            "version": 1
        },
        "f7210df6-380d-597c-a594-72ee0854a798": {
            "created_at": 1759866089134,
            "description": "Acted in The Prince and Me",
            "id": "f7210df6-380d-597c-a594-72ee0854a798",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "luke mably",
            "ontology_valid": False,
            "topological_rank": 0,
            "type": "Entity",
            "updated_at": 1759866135246,
            "version": 1
        },
        "f808d701-98e4-50b8-b21c-c9fc15482898": {
            "created_at": 1759867451494,
            "external_metadata": "{}",
            "id": "f808d701-98e4-50b8-b21c-c9fc15482898",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "mime_type": "text/plain",
            "name": "text_0ba6a84a46eabd72876678e70fc132b7",
            "ontology_valid": False,
            "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_0ba6a84a46eabd72876678e70fc132b7.txt",
            "topological_rank": 0,
            "type": "TextDocument",
            "updated_at": 1759867581439,
            "version": 1
        },
        "fa427fcc-4080-5843-bfb0-089890c7de82": {
            "created_at": 1759867720649,
            "description": "place",
            "id": "fa427fcc-4080-5843-bfb0-089890c7de82",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "place",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759867726469,
            "version": 1
        },
        "fd48be71-1878-56f8-a377-fb877b97acd3": {
            "chunk_index": 0,
            "chunk_size": 2,
            "created_at": 1759867590638,
            "cut_type": "default",
            "id": "fd48be71-1878-56f8-a377-fb877b97acd3",
            "metadata": "{\"index_fields\": [\"text\"]}",
            "ontology_valid": False,
            "text": "4",
            "topological_rank": 0,
            "type": "DocumentChunk",
            "updated_at": 1759867757892,
            "version": 1
        },
        "fee17662-f962-5bba-ab3c-1f889a7a6b40": {
            "created_at": 1759865854318,
            "description": "movie",
            "id": "fee17662-f962-5bba-ab3c-1f889a7a6b40",
            "metadata": "{\"index_fields\": [\"name\"]}",
            "name": "movie",
            "ontology_valid": True,
            "topological_rank": 0,
            "type": "EntityType",
            "updated_at": 1759865895804,
            "version": 1
        }
    },
    "edges": 
    {
        "edge1": {
            "label": "contains",
            "source": "13b2974d-0214-5cc7-b5e7-5ac4bcbb6e49",
            "target": "b661854d-2f9b-5b09-93f9-77be0be05db9"
        },
        "edge10": {
            "label": "is_a",
            "source": "26bd435e-a9d0-545e-af08-1961fa600f55",
            "target": "b1c8236e-7c6c-56a4-985a-a609809cab3f"
        },
        "edge100": {
            "label": "contains",
            "source": "fd48be71-1878-56f8-a377-fb877b97acd3",
            "target": "1f952b2e-6fa5-5842-8d7a-048da390df9b"
        },
        "edge101": {
            "label": "is_a",
            "source": "1f952b2e-6fa5-5842-8d7a-048da390df9b",
            "target": "d61d99ac-b291-5666-9748-3e80e1c8b56a"
        },
        "edge102": {
            "label": "is_part_of",
            "source": "fd48be71-1878-56f8-a377-fb877b97acd3",
            "target": "1612ea96-8870-5cf0-8680-63787271d6e0"
        },
        "edge103": {
            "label": "served_as_president_of",
            "source": "982ac8a9-4a93-598c-a2dc-18af781b6347",
            "target": "72a5d391-5a58-52f2-8058-520d3a5bd2e4"
        },
        "edge104": {
            "label": "assassinated_on",
            "source": "982ac8a9-4a93-598c-a2dc-18af781b6347",
            "target": "1f952b2e-6fa5-5842-8d7a-048da390df9b"
        },
        "edge105": {
            "label": "is_a",
            "source": "9bd785c8-5371-520c-a239-39de82264b0f",
            "target": "06e65008-a5a0-54ab-8399-5d02e1c50294"
        },
        "edge106": {
            "label": "is_a",
            "source": "06e65008-a5a0-54ab-8399-5d02e1c50294",
            "target": "fa427fcc-4080-5843-bfb0-089890c7de82"
        },
        "edge107": {
            "label": "is_a",
            "source": "fa427fcc-4080-5843-bfb0-089890c7de82",
            "target": "7fe7adc6-5a25-519f-ad0b-c14ecedfe6e6"
        },
        "edge108": {
            "label": "made_from",
            "source": "b711a2f8-bdc5-5f87-832a-25022b1e53f4",
            "target": "fd48be71-1878-56f8-a377-fb877b97acd3"
        },
        "edge11": {
            "label": "contains",
            "source": "13b2974d-0214-5cc7-b5e7-5ac4bcbb6e49",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge12": {
            "label": "is_a",
            "source": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "target": "fee17662-f962-5bba-ab3c-1f889a7a6b40"
        },
        "edge13": {
            "label": "is_part_of",
            "source": "13b2974d-0214-5cc7-b5e7-5ac4bcbb6e49",
            "target": "76b73d93-69a8-539b-b220-20ad39f026fd"
        },
        "edge14": {
            "label": "member_of",
            "source": "b1d80755-1dd1-56e7-a372-486d60958d02",
            "target": "abadc643-fea0-5250-ab09-765309cbcc2f"
        },
        "edge15": {
            "label": "was_committed_to",
            "source": "b1d80755-1dd1-56e7-a372-486d60958d02",
            "target": "b5353ef8-9d5c-55c4-8049-41b9d8108760"
        },
        "edge16": {
            "label": "affair_with",
            "source": "b5353ef8-9d5c-55c4-8049-41b9d8108760",
            "target": "b1d80755-1dd1-56e7-a372-486d60958d02"
        },
        "edge17": {
            "label": "character_in",
            "source": "b661854d-2f9b-5b09-93f9-77be0be05db9",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge18": {
            "label": "based_on",
            "source": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "target": "abadc643-fea0-5250-ab09-765309cbcc2f"
        },
        "edge19": {
            "label": "recorded_tribute_at",
            "source": "b1d80755-1dd1-56e7-a372-486d60958d02",
            "target": "26bd435e-a9d0-545e-af08-1961fa600f55"
        },
        "edge2": {
            "label": "is_a",
            "source": "b661854d-2f9b-5b09-93f9-77be0be05db9",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge20": {
            "label": "is_a",
            "source": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
            "target": "7fe7adc6-5a25-519f-ad0b-c14ecedfe6e6"
        },
        "edge21": {
            "label": "is_a",
            "source": "d3d7b6b4-9b0d-52e8-9e09-a9e9cf4b5a4d",
            "target": "7fe7adc6-5a25-519f-ad0b-c14ecedfe6e6"
        },
        "edge22": {
            "label": "is_a",
            "source": "fee17662-f962-5bba-ab3c-1f889a7a6b40",
            "target": "a900fc95-ce79-55da-b56b-0b0b1fe12da4"
        },
        "edge23": {
            "label": "is_a",
            "source": "a900fc95-ce79-55da-b56b-0b0b1fe12da4",
            "target": "7fe7adc6-5a25-519f-ad0b-c14ecedfe6e6"
        },
        "edge24": {
            "label": "made_from",
            "source": "4ff7696e-9e02-5a7e-826a-8ddd833bad18",
            "target": "13b2974d-0214-5cc7-b5e7-5ac4bcbb6e49"
        },
        "edge25": {
            "label": "contains",
            "source": "0e7afef2-5b5f-5c43-87a9-c61e38700ffb",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge26": {
            "label": "is_a",
            "source": "87b90780-ba84-50e2-a755-23e6d86cfe4c",
            "target": "5f710d9d-8811-5cfb-9175-c5c0533b82ca"
        },
        "edge27": {
            "label": "contains",
            "source": "0e7afef2-5b5f-5c43-87a9-c61e38700ffb",
            "target": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0"
        },
        "edge28": {
            "label": "is_a",
            "source": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge29": {
            "label": "contains",
            "source": "0e7afef2-5b5f-5c43-87a9-c61e38700ffb",
            "target": "f7210df6-380d-597c-a594-72ee0854a798"
        },
        "edge3": {
            "label": "contains",
            "source": "13b2974d-0214-5cc7-b5e7-5ac4bcbb6e49",
            "target": "b1d80755-1dd1-56e7-a372-486d60958d02"
        },
        "edge30": {
            "label": "is_a",
            "source": "f7210df6-380d-597c-a594-72ee0854a798",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge31": {
            "label": "contains",
            "source": "0e7afef2-5b5f-5c43-87a9-c61e38700ffb",
            "target": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc"
        },
        "edge32": {
            "label": "is_a",
            "source": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge33": {
            "label": "contains",
            "source": "0e7afef2-5b5f-5c43-87a9-c61e38700ffb",
            "target": "48355aef-4600-5836-a677-65d05d620689"
        },
        "edge34": {
            "label": "is_a",
            "source": "48355aef-4600-5836-a677-65d05d620689",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge35": {
            "label": "contains",
            "source": "0e7afef2-5b5f-5c43-87a9-c61e38700ffb",
            "target": "96d41bf3-11c9-50c5-9094-a27db839e3d7"
        },
        "edge36": {
            "label": "is_a",
            "source": "96d41bf3-11c9-50c5-9094-a27db839e3d7",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge37": {
            "label": "contains",
            "source": "0e7afef2-5b5f-5c43-87a9-c61e38700ffb",
            "target": "664d4c41-2b73-5130-9001-35cb8940b2b5"
        },
        "edge38": {
            "label": "is_a",
            "source": "664d4c41-2b73-5130-9001-35cb8940b2b5",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge39": {
            "label": "contains",
            "source": "0e7afef2-5b5f-5c43-87a9-c61e38700ffb",
            "target": "1c877e38-afdb-5af9-bfa1-c14235256bbe"
        },
        "edge4": {
            "label": "is_a",
            "source": "b1d80755-1dd1-56e7-a372-486d60958d02",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge40": {
            "label": "is_a",
            "source": "1c877e38-afdb-5af9-bfa1-c14235256bbe",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge41": {
            "label": "is_part_of",
            "source": "0e7afef2-5b5f-5c43-87a9-c61e38700ffb",
            "target": "f585f8e0-ef96-53c5-be3f-72cba6465d42"
        },
        "edge42": {
            "label": "acted_in",
            "source": "f3200ed9-17c6-5dd2-8dfb-80aea2e6eae0",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge43": {
            "label": "acted_in",
            "source": "f7210df6-380d-597c-a594-72ee0854a798",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge44": {
            "label": "acted_in",
            "source": "0e4a3e56-5a6b-5b46-8076-38b5f7c457dc",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge45": {
            "label": "cast_member_of",
            "source": "48355aef-4600-5836-a677-65d05d620689",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge46": {
            "label": "cast_member_of",
            "source": "96d41bf3-11c9-50c5-9094-a27db839e3d7",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge47": {
            "label": "acted_in",
            "source": "664d4c41-2b73-5130-9001-35cb8940b2b5",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge48": {
            "label": "directed",
            "source": "1c877e38-afdb-5af9-bfa1-c14235256bbe",
            "target": "87b90780-ba84-50e2-a755-23e6d86cfe4c"
        },
        "edge49": {
            "label": "made_from",
            "source": "232d7e4f-a348-5895-8e41-dec5312ff095",
            "target": "0e7afef2-5b5f-5c43-87a9-c61e38700ffb"
        },
        "edge5": {
            "label": "contains",
            "source": "13b2974d-0214-5cc7-b5e7-5ac4bcbb6e49",
            "target": "b5353ef8-9d5c-55c4-8049-41b9d8108760"
        },
        "edge50": {
            "label": "contains",
            "source": "90c54eb4-362b-5c0c-9331-d232b7711675",
            "target": "66127932-b89f-5cac-bfb3-8132b4119cbd"
        },
        "edge51": {
            "label": "is_a",
            "source": "66127932-b89f-5cac-bfb3-8132b4119cbd",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge52": {
            "label": "contains",
            "source": "90c54eb4-362b-5c0c-9331-d232b7711675",
            "target": "9249c2a3-2ba6-55d6-b2e6-3917982c2ce4"
        },
        "edge53": {
            "label": "is_a",
            "source": "9249c2a3-2ba6-55d6-b2e6-3917982c2ce4",
            "target": "912b273c-683d-53ea-8ffe-aadef0b84237"
        },
        "edge54": {
            "label": "contains",
            "source": "90c54eb4-362b-5c0c-9331-d232b7711675",
            "target": "21d19d74-b14b-5c0a-9272-20904a2f8c73"
        },
        "edge55": {
            "label": "is_a",
            "source": "21d19d74-b14b-5c0a-9272-20904a2f8c73",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge56": {
            "label": "is_part_of",
            "source": "90c54eb4-362b-5c0c-9331-d232b7711675",
            "target": "4130f70e-5e5b-581e-91f1-d60174bd7c94"
        },
        "edge57": {
            "label": "studies_at",
            "source": "66127932-b89f-5cac-bfb3-8132b4119cbd",
            "target": "9249c2a3-2ba6-55d6-b2e6-3917982c2ce4"
        },
        "edge58": {
            "label": "poses_as_student_at",
            "source": "21d19d74-b14b-5c0a-9272-20904a2f8c73",
            "target": "9249c2a3-2ba6-55d6-b2e6-3917982c2ce4"
        },
        "edge59": {
            "label": "made_from",
            "source": "3e1fc0b7-0586-5d76-a13b-98eed72e6877",
            "target": "90c54eb4-362b-5c0c-9331-d232b7711675"
        },
        "edge6": {
            "label": "is_a",
            "source": "b5353ef8-9d5c-55c4-8049-41b9d8108760",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge60": {
            "label": "contains",
            "source": "4e4e97bd-4a6e-539b-9648-95fdedc7ee2b",
            "target": "bfae514a-cfed-5429-8295-a1db7a7e2241"
        },
        "edge61": {
            "label": "is_a",
            "source": "bfae514a-cfed-5429-8295-a1db7a7e2241",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge62": {
            "label": "is_part_of",
            "source": "4e4e97bd-4a6e-539b-9648-95fdedc7ee2b",
            "target": "5fde067d-2a61-579b-a775-9bf52b23053c"
        },
        "edge63": {
            "label": "made_from",
            "source": "9702e91d-6622-5499-9ecd-a067b77d1a17",
            "target": "4e4e97bd-4a6e-539b-9648-95fdedc7ee2b"
        },
        "edge64": {
            "label": "contains",
            "source": "a66adf89-e844-5272-a946-ce9ccf161b6b",
            "target": "5b27b253-0861-567c-a4cd-84f86143a1a1"
        },
        "edge65": {
            "label": "is_a",
            "source": "5b27b253-0861-567c-a4cd-84f86143a1a1",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge66": {
            "label": "contains",
            "source": "a66adf89-e844-5272-a946-ce9ccf161b6b",
            "target": "1d32ad5d-f120-5b70-bafb-1e51e41f3e90"
        },
        "edge67": {
            "label": "is_a",
            "source": "1d32ad5d-f120-5b70-bafb-1e51e41f3e90",
            "target": "d61d99ac-b291-5666-9748-3e80e1c8b56a"
        },
        "edge68": {
            "label": "is_part_of",
            "source": "a66adf89-e844-5272-a946-ce9ccf161b6b",
            "target": "dcc891ef-1e18-5b32-9758-dd822d32f133"
        },
        "edge69": {
            "label": "born_on",
            "source": "5b27b253-0861-567c-a4cd-84f86143a1a1",
            "target": "1d32ad5d-f120-5b70-bafb-1e51e41f3e90"
        },
        "edge7": {
            "label": "contains",
            "source": "13b2974d-0214-5cc7-b5e7-5ac4bcbb6e49",
            "target": "abadc643-fea0-5250-ab09-765309cbcc2f"
        },
        "edge70": {
            "label": "made_from",
            "source": "66e0cbd6-3db5-5178-af77-507bfbab152d",
            "target": "a66adf89-e844-5272-a946-ce9ccf161b6b"
        },
        "edge71": {
            "label": "contains",
            "source": "35055cab-a39f-58fa-89ec-8d385fc80f47",
            "target": "777d1f13-44be-59cb-bebf-95fe1b43bc11"
        },
        "edge72": {
            "label": "is_a",
            "source": "777d1f13-44be-59cb-bebf-95fe1b43bc11",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge73": {
            "label": "contains",
            "source": "35055cab-a39f-58fa-89ec-8d385fc80f47",
            "target": "6fb9b7b8-156a-5559-bd7b-f0bd81bca160"
        },
        "edge74": {
            "label": "is_a",
            "source": "6fb9b7b8-156a-5559-bd7b-f0bd81bca160",
            "target": "07e1512b-5e03-5133-a19b-1f45f2e64c0f"
        },
        "edge75": {
            "label": "contains",
            "source": "35055cab-a39f-58fa-89ec-8d385fc80f47",
            "target": "a2bfbb88-667a-5ef2-ac65-95ada47283f7"
        },
        "edge76": {
            "label": "is_a",
            "source": "a2bfbb88-667a-5ef2-ac65-95ada47283f7",
            "target": "5f710d9d-8811-5cfb-9175-c5c0533b82ca"
        },
        "edge77": {
            "label": "contains",
            "source": "35055cab-a39f-58fa-89ec-8d385fc80f47",
            "target": "acf80a29-7aaf-5f5a-87fb-720408e154b6"
        },
        "edge78": {
            "label": "is_a",
            "source": "acf80a29-7aaf-5f5a-87fb-720408e154b6",
            "target": "5f710d9d-8811-5cfb-9175-c5c0533b82ca"
        },
        "edge79": {
            "label": "is_part_of",
            "source": "35055cab-a39f-58fa-89ec-8d385fc80f47",
            "target": "247e6b40-9b47-550a-83e1-bc4fdb1055b6"
        },
        "edge8": {
            "label": "is_a",
            "source": "abadc643-fea0-5250-ab09-765309cbcc2f",
            "target": "d3d7b6b4-9b0d-52e8-9e09-a9e9cf4b5a4d"
        },
        "edge80": {
            "label": "appeared_in",
            "source": "777d1f13-44be-59cb-bebf-95fe1b43bc11",
            "target": "6fb9b7b8-156a-5559-bd7b-f0bd81bca160"
        },
        "edge81": {
            "label": "acted_in",
            "source": "777d1f13-44be-59cb-bebf-95fe1b43bc11",
            "target": "a2bfbb88-667a-5ef2-ac65-95ada47283f7"
        },
        "edge82": {
            "label": "acted_in",
            "source": "777d1f13-44be-59cb-bebf-95fe1b43bc11",
            "target": "acf80a29-7aaf-5f5a-87fb-720408e154b6"
        },
        "edge83": {
            "label": "made_from",
            "source": "a4e9d9a8-7bc4-57f3-8135-0220c8be2f4b",
            "target": "35055cab-a39f-58fa-89ec-8d385fc80f47"
        },
        "edge84": {
            "label": "is_part_of",
            "source": "8cfe8577-7e46-5d01-9fac-128e9ec5d969",
            "target": "6848eb4b-e3f5-5c5d-b68b-91a6f3ecc48c"
        },
        "edge85": {
            "label": "made_from",
            "source": "9a549ea8-90bd-5e0c-8c89-a496a570a084",
            "target": "8cfe8577-7e46-5d01-9fac-128e9ec5d969"
        },
        "edge86": {
            "label": "is_part_of",
            "source": "a3be1b91-8617-51a1-ac6c-33c89e7564cb",
            "target": "33123e17-ef57-5eab-821b-983fdf32b0c2"
        },
        "edge87": {
            "label": "made_from",
            "source": "df23bf40-916e-551c-bd98-9d7ada0706d9",
            "target": "a3be1b91-8617-51a1-ac6c-33c89e7564cb"
        },
        "edge88": {
            "label": "is_part_of",
            "source": "60400025-6197-59e8-a985-b020912a6521",
            "target": "36f04799-e348-5658-8927-3779ac6171a1"
        },
        "edge89": {
            "label": "made_from",
            "source": "0fd1eeaa-69e9-55bc-9d03-8e234a8c95ae",
            "target": "60400025-6197-59e8-a985-b020912a6521"
        },
        "edge9": {
            "label": "contains",
            "source": "13b2974d-0214-5cc7-b5e7-5ac4bcbb6e49",
            "target": "26bd435e-a9d0-545e-af08-1961fa600f55"
        },
        "edge90": {
            "label": "contains",
            "source": "76bd6a74-912c-546e-bd5b-d38273cdc650",
            "target": "1c877e38-afdb-5af9-bfa1-c14235256bbe"
        },
        "edge91": {
            "label": "is_part_of",
            "source": "76bd6a74-912c-546e-bd5b-d38273cdc650",
            "target": "a9ca3cc1-b6ba-5497-bea8-aeffa3a322ab"
        },
        "edge92": {
            "label": "made_from",
            "source": "e2011dee-b9d7-53bc-ae22-bba4ca2fe09b",
            "target": "76bd6a74-912c-546e-bd5b-d38273cdc650"
        },
        "edge93": {
            "label": "contains",
            "source": "a494b807-21e0-5bc2-9d7d-5a206d3b6c8c",
            "target": "1c877e38-afdb-5af9-bfa1-c14235256bbe"
        },
        "edge94": {
            "label": "is_part_of",
            "source": "a494b807-21e0-5bc2-9d7d-5a206d3b6c8c",
            "target": "f808d701-98e4-50b8-b21c-c9fc15482898"
        },
        "edge95": {
            "label": "made_from",
            "source": "c404dd9b-4545-5a30-81e0-cd700f696e21",
            "target": "a494b807-21e0-5bc2-9d7d-5a206d3b6c8c"
        },
        "edge96": {
            "label": "contains",
            "source": "fd48be71-1878-56f8-a377-fb877b97acd3",
            "target": "982ac8a9-4a93-598c-a2dc-18af781b6347"
        },
        "edge97": {
            "label": "is_a",
            "source": "982ac8a9-4a93-598c-a2dc-18af781b6347",
            "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134"
        },
        "edge98": {
            "label": "contains",
            "source": "fd48be71-1878-56f8-a377-fb877b97acd3",
            "target": "72a5d391-5a58-52f2-8058-520d3a5bd2e4"
        },
        "edge99": {
            "label": "is_a",
            "source": "72a5d391-5a58-52f2-8058-520d3a5bd2e4",
            "target": "9bd785c8-5371-520c-a239-39de82264b0f"
        }
    }
}

EVALUATION_RESULT = {
    "evaluation": {
        "actual_output": "The park that links Salisbury Woodland Gardens with a zoo was designed and built in the 1920s under the supervision of Thomas Mawson. The last letter of his first name 'Thomas' is 's', which has an ASCII code of 115.",
        "expected_output": "115",
        "input": "What is the ASCII code of the last letter of the first name of the person who designed and built the park which links Salisbury Woodland Gardens with a zoo?",
        "metrics": [
            {
                "metric_name": "Answer Relevancy",
                "passed": True,
                "reasoning": "The score is 1.00 because the response directly addresses the input question by providing the ASCII code for the specified character, without including any irrelevant information.",
                "score": 1
            },
            {
                "metric_name": "Faithfulness",
                "passed": True,
                "reasoning": "The score is 1.00 because there are no contradictions present, indicating that the 'actual output' aligns perfectly with the information in the 'retrieval context'. This demonstrates a high level of faithfulness and accuracy.",
                "score": 1
            }
        ],
        "success": True
    },
}

#######################################################################################################
#######################################################################################################
#######################################################################################################
def worker_mock_processamento(task_id, dados_para_processar):
    try:

        print("DADOS RECEBIDOS DO FRONT:", dados_para_processar)

        tasks[task_id]['status'] = 'PROCESSING'
        time.sleep(1)

        tipoProcessamento = dados_para_processar["processingType"]["value"]

        match tipoProcessamento:
                case 1:
                    resultado_analise = analisar_grafo(FIXED_RESULT1["nodes"], FIXED_RESULT1["edges"])
                    tasks[task_id]['status'] = 'SUCCESS'
                    tasks[task_id]['result'] = FIXED_RESULT1 | resultado_analise | EVALUATION_RESULT           
                case 2:
                    resultado_analise = analisar_grafo(FIXED_RESULT2["nodes"], FIXED_RESULT2["edges"])
                    tasks[task_id]['status'] = 'SUCCESS'
                    tasks[task_id]['result'] = FIXED_RESULT2 | resultado_analise | EVALUATION_RESULT
                case 3:
                    resultado_analise = analisar_grafo(FIXED_RESULT3["nodes"], FIXED_RESULT3["edges"])
                    tasks[task_id]['status'] = 'SUCCESS'
                    tasks[task_id]['result'] = FIXED_RESULT3 | resultado_analise | EVALUATION_RESULT           
                case 4:
                    resultado_analise = analisar_grafo(FIXED_RESULT4["nodes"], FIXED_RESULT4["edges"])
                    tasks[task_id]['status'] = 'SUCCESS'
                    tasks[task_id]['result'] = FIXED_RESULT4 | resultado_analise | EVALUATION_RESULT 
    except Exception as e:
        app.logger.error(f"Erro na tarefa simulada {task_id}: {e}")
        tasks[task_id]['status'] = 'FAILURE'
        tasks[task_id]['result'] = {"erro": "Ocorreu um erro no worker de teste.", "detalhes": str(e)}


#######################################################################################################
#######################################################################################################
#######################################################################################################
@app.route('/runquestion', methods=['POST'])
def run_question_async_mock():
    try:
        dados_recebidos = request.get_json()
        if dados_recebidos is None:
            return jsonify({"erro": "Corpo da requisição inválido ou não é JSON."}), 400
    except Exception:
        return jsonify({"erro": "Erro ao decodificar o JSON da requisição."}), 400
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'PENDING', 'result': None}
    thread = threading.Thread(target=worker_mock_processamento, args=(task_id,dados_recebidos))
    thread.start()
    return jsonify({"task_id": task_id}), 202


#######################################################################################################
#######################################################################################################
#######################################################################################################
@app.route('/status/<task_id>', methods=['GET'])
def get_status_mock(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"erro": "ID da tarefa não encontrado."}), 404
    response_data = {
        "task_id": task_id,
        "status": task['status']
    }
    if task['status'] in ['SUCCESS', 'FAILURE']:
        response_data['result'] = task['result']   
    return jsonify(response_data), 200



#######################################################################################################
#######################################################################################################
#######################################################################################################
def processar_comparacoes(comparison_id, dados_para_processar):
    try:
        comparisons[comparison_id]['status'] = 'PROCESSING'
        
        idtask_grafo1 = dados_para_processar["idtask_grafo1"]
        idtask_grafo2 = dados_para_processar["idtask_grafo2"]

        grafo1 = tasks[idtask_grafo1]['result']
        grafo2 = tasks[idtask_grafo2]['result']
        #grafo1 = FIXED_RESULT1
        #grafo2 = FIXED_RESULT2

        resultado_analise = processar_grafos_e_gerar_saida(grafo1, grafo2) #analisar_grafo_heatmap(grafo1, grafo2)
        comparisons[comparison_id]['status'] = 'SUCCESS'
        comparisons[comparison_id]['result'] = json.loads(resultado_analise)            
    except Exception as e:
        app.logger.error(f"Erro na tarefa simulada {comparison_id}: {e}")
        comparisons[comparison_id]['status'] = 'FAILURE'
        comparisons[comparison_id]['result'] = {"erro": "Ocorreu um erro no processamento da comparacao.", "detalhes": str(e)}


#######################################################################################################
#######################################################################################################
#######################################################################################################
@app.route('/runcomparison', methods=['POST'])
def run_comparasion():
    try:
        dados_recebidos = request.get_json()
        #print(dados_recebidos)
        if dados_recebidos is None:
            return jsonify({"erro": "Corpo da requisição inválido ou não é JSON."}), 400
    except Exception:
        return jsonify({"erro": "Erro ao decodificar o JSON da requisição."}), 400
    
    comparison_id = str(uuid.uuid4())
    comparisons[comparison_id] = {'status': 'PENDING', 'result': None}
    thread = threading.Thread(target=processar_comparacoes, args=(comparison_id,dados_recebidos))
    thread.start()
    return jsonify({"comparison_id": comparison_id}), 202


#######################################################################################################
#######################################################################################################
#######################################################################################################
@app.route('/getcomparison/<comparison_id>', methods=['GET'])
def get_comparasion(comparison_id):
    comp = comparisons.get(comparison_id)
    if not comp:
        return jsonify({"erro": "ID da comparação não encontrado."}), 404
    response_data = {
        "comparison_id": comparison_id,
        "status": comp['status']
    }
    if comp['status'] in ['SUCCESS', 'FAILURE']:
        response_data['result'] = comp['result']   
    return jsonify(response_data), 200

#######################################################################################################
#######################################################################################################
#######################################################################################################

@app.route('/static/<filename>')
def get_image(filename):
    """Serve o arquivo de imagem do diretório de imagens."""
    return send_from_directory(IMAGE_DIR, filename)

#######################################################################################################
#######################################################################################################
#######################################################################################################


@app.route('/modelos', methods=['GET'])
def obter_modelos():
    ollama_manager = OllamaModelManager()
    modelos = ollama_manager.listar_modelos()
    resposta = {"modelos": modelos}
    
    return jsonify(resposta), 200

#######################################################################################################
#######################################################################################################
#######################################################################################################

if __name__ == '__main__':
    app.run(debug=True, port=5001)

