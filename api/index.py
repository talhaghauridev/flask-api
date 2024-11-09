import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
print(file,parent,root)
sys.path.append(str(root))

from app import create_app  
app = create_app()

if __name__ == '__main__':
    print("App run in production")
    app.run(debug=False)