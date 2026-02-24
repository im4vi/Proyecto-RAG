from src.infrastructure.configuration.config import Config
from src.infrastructure.configuration.container import get_index_documents_use_case


def main():
    Config.ensure_directories()
    
    # Obtener caso de uso del container
    use_case = get_index_documents_use_case()
    
    # Ejecutar indexación
    use_case.execute(Config.RAW_DATA_PATH)


if __name__ == "__main__":
    main()
