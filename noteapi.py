from note import note

if __name__ == '__main__':
    #from waitress import serve
    #serve(note, port="80")
    note.run(debug=False, port="80")
