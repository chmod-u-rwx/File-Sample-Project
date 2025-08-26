
from pydantic import BaseModel, Field, ValidationError
import hashlib
import json
import time
import sys

class FileInputModel(BaseModel):
    qty: int = Field(...)
    text: str = Field(...)


def process(text: str, qty: int):
    time.sleep(2)
    result = text
    for _ in range(qty):
        result = hashlib.sha256(result.encode()).hexdigest()
    return {"input": text, "result": result}

if __name__ == "__main__":
    input_path = "./input.json"
    output_path = "./output.json"
    error_path = "./error.json"
    try:
        with open(input_path, "r") as input_file:
            raw_data = json.load(input_file)
            data = FileInputModel(**raw_data)

        with open(output_path, "w") as output_file:
            output = process(data.text, data.qty)
            json.dump(output, output_file)
        
        sys.exit(0)
    except (json.JSONDecodeError, ValidationError) as e:
        with open(error_path, "w") as error_file:
                error = {"error": "Invalid Args", "detail": str(e)}
                json.dump(error, error_file)
        sys.exit(1)
    except Exception as e:
        with open(error_path, "w") as error_file:
                error = {"error": "Unexpected Error Ocurred", "detail": str(e)}
                json.dump(error, error_file)
        sys.exit(2)
