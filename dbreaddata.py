import _mysql
from modulenorm.modNormalize import normalize
from modulenorm.modTokenizing import tokenize

# membuka koneksi database
db = _mysql.connect(
	user="root",
	passwd="",
	host="127.0.0.1",
	db="twitterdata"
	)

# mengambil data
db.query("SELECT * FROM dataset")
result = db.store_result()
# print(result.fetch_row())

# menampilkan
no = 1
for row in result.fetch_row(maxrows=0):
	text = row[6]
	text_decode = str(text.decode('utf-8', 'ignore').encode('cp850', 'replace').decode('cp850'))

	usenorm = normalize()
	text_norm = usenorm.enterNormalize(text_decode) # normalisasi enter, 1 revw 1 baris
	# text_norm = usenorm.lowerNormalize(text_norm) # normalisasi huruf besar ke kecil
	text_norm = usenorm.repeatcharNormalize(text_norm) # normalisasi titik yang berulang
	text_norm = usenorm.linkNormalize(text_norm) # normalisasi link dalam text
	text_norm = usenorm.spacecharNormalize(text_norm) # normalisasi spasi karakter
	text_norm = usenorm.ellipsisNormalize(text_norm) # normalisasi elepsis (…)

	tok = tokenize() # panggil modul tokenisasi
	text_norm = tok.WordTokenize(text_norm) # pisah tiap kata pada kalimat

	text_norm = usenorm.spellNormalize(text_norm) # cek spell dari kata perkata
	text_norm = usenorm.wordcNormalize(text_norm,2) # menyambung kata (malam-malam) (param: textlist, jmlh_loop)
	# text_norm = usenorm.stemmingNormalize(text_norm,'word') # mengubah ke bentuk kata dasar (text, type_data)

	text_norm = ' '.join(text_norm) # menggabung kalimat tokenize dengan separate spasi

	text_norm = usenorm.emoticonNormalize(text_norm) # menggabung struktur emoticon yang terpisah ([: - )] = [:-)])

	# walking2
	# konfer @ ke at untuk penunjuk tempat

	output = open("output.txt","a")
	output.write(str(text_norm))
	output.write('\n')
	output.close()

	# print(no)
	no += 1

# tutup koneksi
# cur.close()
db.close()
