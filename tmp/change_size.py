import sys; open( sys.argv[2], "wb" ).write( open( sys.argv[1], "rb" ).read( 4096 ) )
