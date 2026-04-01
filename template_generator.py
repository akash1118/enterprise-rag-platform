import os

# Define folder structure
project_structure = {
    "rag-platform": {
        "api": {
            "routes": {},
            "middleware": {}
        },
        "services": {
            "ingestion": {},
            "retrieval": {},
            "llm_gateway": {},
            "guardrails": {}
        },
        "core": {
            "config": {},
            "logging": {}
        },
        "models": {},
        "workers": {},
        "infra": {
            "docker": {},
            "k8s": {}
        },
        "experiments": {
            "chunking_eval": {},
            "retrieval_eval": {}
        },
        "tests": {}
    }
}


def create_structure(base_path, structure):
    for name, sub_structure in structure.items():
        path = os.path.join(base_path, name)
        
        # Create directory
        os.makedirs(path, exist_ok=True)
        print(f"Created directory: {path}")
        
        # Create __init__.py for Python packages (except infra/experiments)
        if name not in ["docker", "k8s"]:
            init_file = os.path.join(path, "__init__.py")
            with open(init_file, "w") as f:
                f.write("# init\n")
        
        # Recursively create subdirectories
        if isinstance(sub_structure, dict):
            create_structure(path, sub_structure)


if __name__ == "__main__":
    create_structure(".", project_structure)
    print("RAG project structure created successfully!")