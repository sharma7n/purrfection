import os
import sys

from app import app

key = sys.argv[1]

if __name__ == '__main__':
	if key.lower() == 'run':
		port = int(os.environ.get('PORT', 5000))
		app.run(host='0.0.0.0', port=port)