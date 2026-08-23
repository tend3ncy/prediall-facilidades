"""
Script para inicializar a base de conhecimento (RAG).
Indexa os documentos de procedimentos no ChromaDB.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.rag import carregar_base_conhecimento, buscar_contexto


def main():
    print("=" * 60)
    print("  PrediALL Facilidades — Setup Base de Conhecimento (RAG)")
    print("=" * 60)
    print()
    print("Indexando documentos no ChromaDB...")
    print()

    total = carregar_base_conhecimento()

    print(f"✅ {total} documentos indexados com sucesso!")
    print()
    print("Testando busca vetorial...")
    print()

    # Testes de busca
    testes = [
        "ar condicionado vazando água",
        "tomada com faísca no escritório",
        "banheiro entupido",
        "cheiro de gás no galpão",
        "cadeira quebrada",
        "portão da doca travado",
    ]

    for query in testes:
        resultado = buscar_contexto(query, n_resultados=2)
        print(f"🔍 Query: '{query}'")
        if resultado:
            # Mostra apenas as primeiras 100 chars de cada resultado
            linhas = resultado.split("---")
            for linha in linhas[:2]:
                preview = linha.strip()[:100]
                if preview:
                    print(f"   → {preview}...")
        else:
            print("   → Nenhum resultado")
        print()

    print("=" * 60)
    print("✅ Base de conhecimento pronta!")
    print("   Os dados estão em ./chroma_data/")
    print("=" * 60)


if __name__ == "__main__":
    main()
