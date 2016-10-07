import StringIO
import json
import logging
import random
import urllib
import urllib2

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

# Create extoken.py and write
# TOKEN = 'YOUR_BOT_TOKEN_HERE'
from extoken import TOKEN

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

URL_ESAMI = 'https://www.studenti.ict.uniba.it/esse3/ListaAppelliOfferta.do?btnSubmit&fac_id=1097&cds_id=10098&docente_id='


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        try:
        	message = body['message']
        except:
        	message = body['edited_message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']
        privacy = chat['type']

        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None, stk=None, audio=None, doc=None, fw=None, chat=None, chat1=None, chat2=None, chat3=None, chat4=None, chat5=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg,
                    'disable_web_page_preview': 'true',
                    'parse_mode': 'HTML',
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            elif stk:
                resp = urllib2.urlopen(BASE_URL + 'sendSticker', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'sticker': stk,
                })).read()
            elif audio:
                resp = urllib2.urlopen(BASE_URL + 'sendAudio', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'audio': audio,
                })).read()
            elif doc:
                resp = urllib2.urlopen(BASE_URL + 'sendDocument', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'document': doc,
                })).read()
            elif fw:
                resp = urllib2.urlopen(BASE_URL + 'forwardMessage', urllib.urlencode({
                    'chat_id': fw,
                    'from_chat_id': str(chat_id),
                    'message_id': str(message_id),
                    'parse_mode': 'HTML',
                })).read()
            elif chat:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': '-12787170',
                    'text': chat.replace("=PBZZ=", "").encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'parse_mode': 'HTML',
                })).read()
            elif chat1:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': '-36729866',
                    'text': chat1.replace("=STUDENTIPER=", "").encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'parse_mode': 'HTML',
                })).read()
            elif chat2:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': '-12604594',
                    'text': chat2.replace("=LAPA=", "").encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'parse_mode': 'HTML',
                })).read()
            elif chat3:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': '-7284886',
                    'text': chat3.replace("=3LZ=", "").encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'parse_mode': 'HTML',
                })).read()
            elif chat4:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': '-23982686',
                    'text': chat4.replace("=1AK=", "").encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'parse_mode': 'HTML',
                })).read()
            elif chat5:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': '-18336711',
                    'text': chat5.replace("=1LZ=", "").encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'parse_mode': 'HTML',
                })).read()
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)

        if text.startswith('/'):
            if text.lower() == '/start' or text.lower() == '/start@sarcinellobot':
                reply('<b>Sarcinello</b> attivato.\nInvia /comandi per elencare le funzioni disponibili.\nPer contattare mio padre: @nicoserafino')
                setEnabled(chat_id, True)
            elif text.lower() == '/stop' or text.lower() == '/stop@sarcinellobot':
                reply('<b>Sarcinello</b> disattivato.\nInvia /start per attivarlo.')
                setEnabled(chat_id, False)
        if text.lower() == '/comandi' or text.lower() == '/comandi@sarcinellobot':
            reply('Ciao! sono il <b>Sarcinello</b>. Per contattare mio padre: @nicoserafino\n\n/start per attivare il Sarcinello\n/stop per disattivarlo\n\nsuggerimento - Suggeriscimi una funzione\n\nsegreteria\n\naula studio - per gli orari delle aule studio\n\nbiblioteca - per gli orari della biblioteca\n\nmappa del policlinico\n\nade, pezzolla, carratù\n\ntasse, iscrizioni, simulatore\n\nscandeza rate\n\nisee, iseu\n\nadisu, bando\n\nfrequenze, badge\n\npropedeuticità\n\nmodulistica\n\norari, calendario\n\nprogrammi\n\n appelli\n\n programma di [disciplina] - ad esempio "programma di chimica"\n\nnodbis, laurea\n\nprogress test')

        # CUSTOMIZE FROM HERE 
		# Testo			reply('testo')
        # Immagini		reply(img=urllib2.urlopen('https://telegram.org/img/t_logo.png').read())
		# Sticker		reply(stk='file_id')
		# Audio			reply(audio='file_id')
		# Documenti		reply(doc='file_id')

		#   elif privacy == 'private':
		#		reply(fw='43591247')

		# TODO
		# if 'appell' in text.lower() and 'capuano' in text.lower():
		# 	reply(URL_ESAMI + '1267')

        elif text.lower() != 'suggerimento' and 'suggerimento' in text.lower():
			reply(fw='43591247')
			reply('Grazie per il tuo suggerimento!')
        elif text.startswith('=PBZZ='):
			reply(chat=text)
        elif text.startswith('=STUDENTIPER='):
			reply(chat1=text)
        elif text.startswith('=LAPA='):
			reply(chat2=text)
        elif text.startswith('=3LZ='):
			reply(chat3=text)
        elif text.startswith('=1AK='):
			reply(chat4=text)
        elif text.startswith('=1LZ='):
			reply(chat5=text)
        else:
            if getEnabled(chat_id):
				#if 'elezion' in text.lower() or 'voto' in text.lower() or 'vota' in text.lower() or 'votazione' in text.lower() or 'votare' in text.lower() or 'candidat' in text.lower() or 'rappresentan' in text.lower() or 'lista' in text.lower() or 'liste' in text.lower() or '18' in text.lower() or '19' in text.lower() or 'maggio' in text.lower() or 'persempre' in text.lower() or 'per sempre' in text.lower() or 'studentiper' in text.lower() or 'UP' in text.lower() or 'seggi' in text.lower() or 'scheda' in text.lower() or 'elettorale' in text.lower():
				#	reply('Il 18 e il 19 maggio vota StudentiPer (UP ai centrali).\n\nLe nostre conquiste..')
				#	reply(img=urllib2.urlopen('http://creop.altervista.org/Media/Foto/elezioni1.jpg').read())
				#	reply('E quello che continueremo a fare..#PerSempre')
				#	reply(img=urllib2.urlopen('http://creop.altervista.org/Media/Foto/elezioni2.jpg').read())
				if ('nico' in text.lower().split() or 'quaranta' in text.lower().split() or '40' in text.split()) and not 'la nico' in text.lower():
					reply(stk='BQADBAADGwADTyaZAjUU-thrRuh9Ag')
				if 'pita' in text.lower():
					reply('Pita è sfigata ' + u'\U0001F62D'.encode('utf-8'))
				if 'gestione' in text.lower() or 'gestitevi' in text.lower():
					reply(stk='BQADBAADHQADTyaZAiyn9ScUMAh6Ag')
				if 'parisi' in text.lower() or ( 'st' in text.lower() and 'bene' in text.lower() ):
					reply('Parisi sta bene!')
				if 'lucilla' in text.lower():
					reply('Lucilla ti guarda.')
				if 'convenzioni' in text.lower():
					reply('Tutti i vantaggi che offre la StudentiPer Card. Richiedila in auletta!\n http://app.studentiper.it/convenzioni.html')
				if 'auguri' in text.lower():
					reply('Auguri!')
				if text.lower() == 'suggerimento':
					reply('Per suggerire scrivi qualcosa dopo la parola \'suggerimento\'')
				if 'mappa' in text.lower() or ('mappa' in text.lower() and 'policlinico' in text.lower()):
					reply(img=urllib2.urlopen('http://creop.altervista.org/Sarcinellobot/Media/Foto/mappa.jpg').read())
				if 'erasmus' in text.lower():
					reply('Tutte le info riguardanti il programma Erasmus per gli studenti Uniba sono disponibili sul sito web http://uniba.llpmanager.it/studenti/')
				if 'segreteria' in text.lower():
					reply('La segreteria è aperta dal Lunedi al Venerdi mattina dalle 10 alle 12. Martedi e Giovedi pomeriggio dalle 15 alle 17.')
				if 'rata' in text.lower() or 'rate' in text.lower() or ('scade' in text.lower() and 'rat' in text.lower()):
					reply(img=urllib2.urlopen('http://creop.altervista.org/Sarcinellobot/Media/Foto/rate.jpg').read())
				if ('mail' in text.lower() and 'prof' in text.lower()) or 'ricevimento' in text.lower():
					reply('Questo sito riporta indirizzi e-mail e curricula (cliccando sul nome) dei professori.\n http://www.medicina.uniba.it/personale/index.jsp \nSolitamente nel curriculum è riportato l\'orario di ricevimento abituale.')
				if 'ade' in (text.lower()).split() or 'ade?' in (text.lower()).split() or 'pezzolla' in text.lower() or 'carrat' in text.lower():
					reply('Le ADE sono attività didattiche elettive, cioè seminari e convegni che si tengono al policlinico in orari che non interferiscano con l\'attività didattica ordinaria. Con la partecipazione a questi eventi si ottengono attestati e CFU (spesso 0.3CFU a sessione). Raggiunto il numero di CFU in ADE previsti dal piano di studio per l\'anno in corso, gli attestati vanno consegnati alle Prof. Carratù (AK) o Pezzolla (LZ) come segue.\n\nPER GLI AK\nLa prof.ssa Carratù riceve lunedì e mercoledì dalle 9.30 alle 12.30 primo piano degli istituti biologici.\n\nPER GLI LZ\nLa prof.ssa Pezzolla riceve dal 13 settembre settembre il martedi dalle 10 alle 12 al quarto piano del padiglione Asclepios (ingresso Pronto Soccorso).\n\nIl modulo ADE va consegnato alle professoresse entro il 30 settembre con gli attestati originali in allegato. Successivamente il solo modulo, privo degli attestati, va ritirato (AK il giovedì, LZ il martedì della settimana successiva con lo stesso orario)e consegnato in segreteria entro il 31 ottobre.')
				if 'moduli' in text.lower() or 'modulo' in text.lower():
					reply('Segui questo link per tutta la modulistica http://goo.gl/FnFD0C')
				if 'cus' in text.lower().split():
					reply('Il CUS, Centro Universitario Sportivo, offre numerosi vantaggi per gli studenti dell\'Uniba. L\'iscrizione è di 20€ (15€ se è la tua prima iscrizione). Queste le convenzioni:')
					reply(img=urllib2.urlopen('http://creop.altervista.org/Sarcinellobot/Media/Foto/cus.jpg').read())
				if 'aula' in text.lower() and 'studio' in text.lower() or ('sal' in text.lower() and 'lettur' in text.lower()):
					reply('Gli orari di apertura dell\'aula studio del polinfunzionale sono quelli indicati nell\'immagine seguente.\nL\'aula studio del dipartimento di Biochimica è aperta dalle 8.15 alle 18.00.\nPer la biblioteca centrale digita \'biblioteca\'')
					reply(img=urllib2.urlopen('http://creop.altervista.org/Sarcinellobot/Media/Foto/polifunzionale.jpg').read())
				if 'biblioteca' in text.lower():
					reply('Orari biblioteca centrale: http://goo.gl/948hLn\nPer l\'aula studio digita \'aula studio\'')
				if 'propedeuticit' in text.lower() or 'propedeutic' in text.lower():
					reply(img=urllib2.urlopen('http://creop.altervista.org/Sarcinellobot/Media/Foto/propedeut.jpg').read())
				if 'nodbis' in text.lower() or 'laurea' in text.lower():
					reply('Leggi qui il regolamento nodbis http://goo.gl/bkCtjD')
					reply(img=urllib2.urlopen('http://creop.altervista.org/Sarcinellobot/Media/Foto/nodbis.jpg').read())
				if 'progress' in text.lower() and 'test' in text.lower():
					reply('Il progress test è una prova nazionale che consiste in due quiz a risposta multipla, ognuno da 150 domande (150 di area pre-clinica e 150 di area clinica).\n\nLa frequenza della giornata è assegnata purché lo studente consegni le risposte dopo almeno 45 minuti dall\'inizio di ogni prova. Se lo studente supera il punteggio medio del proprio anno, valutato sulla base dei test svolti negli anni precedenti, sarà assegnato un punto aggiuntivo nella media dei voti per il calcolo del voto di presentazione alla seduta di Laurea.\n(*nessun voto sarà formalmente modificato)')
				if 'adisu' in text.lower() or ('borsa' in text.lower() and 'studio' in text.lower()) or 'bando' in (text.lower()).split():
					reply('BANDO ADISU 2015/16: http://goo.gl/Py2HYR \nSCADENZE: http://goo.gl/nTikvg \n\nL\'ufficio in Via Giustino Fortunato è aperto dal lunedì al venerdì dalle 9 alle 12. Il martedì e il giovedì anche il pomeriggio dalle 15 alle 16.')
				if 'tasse' in text.lower().split() or 'immatricolazion' in text.lower():
					reply('PAGA PIAGA!\nSe cerchi il simulatore tasse del sito UNIBA segui questo link: https://csi.ict.uniba.it/simulatoretasse')
					reply('II rata prorogata al 20 ottobre.\nIII rata rateizzata 50% entro il 20 novembre e 50% entro il 28 febbraio.\nI rata 2016/17 entro il 20 dicembre.')
				if 'iscrizion' in text.lower() or 'sbarrament' in text.lower():
					reply('Per iscriversi ad anni successivi occorrono i seguenti requisiti entro Febbraio 2017')
					reply(img=urllib2.urlopen('http://creop.altervista.org/Sarcinellobot/Media/Foto/sbarramenti.png').read())
				if 'simulatore' in text.lower():
					reply('Per il simulatore tasse by StudentiPer segui questo link: http://goo.gl/g6IRLp')
				if 'isee' in text.lower() or 'iseu' in text.lower():
					reply('L\'ISEE per prestazioni universitarie va richiesto al CAF (dovrai ripassare 15 giorni dopo per ricevere copia cartacea). Successivamente l\'uniba lo recupera telematicamente, quindi non c\'è alcuna documentazione da consegnare in segreteria. Per i servizi ADISU, invece, occorre copia cartacea.\nScrivi "iscrizione" per info sull\'iscrizione ad anni successivi.')
				if 'frequenz' in text.lower() or 'intermedi' in text.lower() or 'badge' in text.lower():
					reply('Il badge non sarà utilizzato nemmeno quest\'anno (ascolta l\'audio).\nLe frequenze delle prove intermedie non sono richieste per sostenere l\'esame. L\'ex primo anno ha solo quelle di citologia, ma per un errore della segreteria.')
				if 'calendario' in text.lower() or ('orari' in text.lower() and not 'segreteria' in text.lower() and not 'ricevimento' in text.lower() and not 'biblioteca' in text.lower() and not 'aula' in text.lower()):
#					reply('Gli orari del secondo semestre A.A. 2016-2017 non sono ancora disponibili')
					reply('Per quale anno? Ora disponibili:\n /I_AK \n /I_LZ \n /II_AK \n /II_LZ \n /III_AK \n /III_LAPA \n /III_PBZZ \n /IV_AK \n /IV_LZ \n /V_AK \n /V_LZ')
				if 'materiale' in text.lower() and 'didattico' in text.lower():
					reply('Segui questo link per l\'archivio su Drive (secondo anno LZ) https://goo.gl/xGceWn')
				if text == '/I_AK' or text == '/I_AK@sarcinellobot':
					reply('Orari I_AK: https://goo.gl/PX1DFN')
				if text == '/I_LZ' or text == '/I_LZ@sarcinellobot':
					reply('Orari I_LZ: https://goo.gl/3Ug8Wc')
				if text == '/II_AK' or text == '/II_AK@sarcinellobot':
					reply('Orari II_AK: https://goo.gl/8hhgls')
				if text == '/II_LZ' or text == '/II_LZ@sarcinellobot':
					reply('Orari II_LZ: https://goo.gl/eTQ3z2')
				if text == '/III_AK-A' or text == '/III_AK-A@sarcinellobot':
					reply('Orari III_AK-A: https://goo.gl/JTTauS')
				if text == '/III_AK-B' or text == '/III_AK-B@sarcinellobot':
					reply('Orari III_AK-B: https://goo.gl/sdPumR')
				if text == '/III_LAPA' or text == '/III_LAPA@sarcinellobot':
					reply('Orari III_LAPA: https://goo.gl/TMyCTV')
				if text == '/III_PBZZ' or text == '/III_PBZZ@sarcinellobot':
					reply('Orari III_PBZZ: https://goo.gl/pI58BE')
				if text == '/IV_AK' or text == '/IV_AK@sarcinellobot':
					reply('Orari IV_AK: https://goo.gl/vVsZSG')
				if text == '/IV_LZ' or text == '/IV_LZ@sarcinellobot':
					reply('Orari IV_LZ: https://goo.gl/YFAazr')
				if text == '/V_AK' or text == '/V_AK@sarcinellobot':
					reply('Orari V_AK: https://goo.gl/PkJJ2e')
				if text == '/V_LZ' or text == '/V_LZ@sarcinellobot':
					reply('Orari V_LZ: https://goo.gl/zFo4vk')
				if text == '/VI_AK' or text == '/VI_AK@sarcinellobot':
					reply('Orari VI_AK: https://goo.gl/bHYCr1')
				if text == '/VI_LZ' or text == '/VI_LZ@sarcinellobot':
					reply('Orari VI_LZ: https://goo.gl/AhfW47')
				if text.lower() == 'anatomia' or ('anatomia' in text.lower() and 'appell' in text.lower()):
					reply('Incubo!')
				if 'appelli' in text.lower() or 'appello' in text.lower():
					reply('Cerchi gli appelli per quale anno? Ora disponibili:\n /esami_I \n /esami_II \n /esami_III')
				if text == '/esami_I' or text == '/esami_I@sarcinellobot':
					reply(img=urllib2.urlopen('http://creop.altervista.org/Sarcinellobot/Media/Foto/esami1.jpg').read())
				if text == '/esami_II' or text == '/esami_II@sarcinellobot':
					reply(img=urllib2.urlopen('http://creop.altervista.org/Sarcinellobot/Media/Foto/esami2.jpg').read())
				if text == '/esami_III' or text == '/esami_III@sarcinellobot':
					reply(img=urllib2.urlopen('http://creop.altervista.org/Sarcinellobot/Media/Foto/esami3.jpg').read())
				if 'programmi' in text.lower():
					reply('Segui questo link per tutti i programmi http://goo.gl/v69OQt')
				if 'programm' in text.lower() and 'umane' in text.lower():
					reply('Segui questo link per il programma di Scienze Umane http://goo.gl/6ZUh5W')
				if 'programm' in text.lower() and ( 'biologia' in text.lower() or 'genetica' in text.lower() ) and 'micro' not in text.lower():
					reply('Segui questo link per il programma di Biologia e Genetica http://goo.gl/h8TWlc')
				if 'programm' in text.lower() and ( 'fisica' in text.lower() or 'informatica' in text.lower() ):
					reply('Segui questo link per il programma di Fisica e Informatica http://goo.gl/VV8PSG')
				if 'programm' in text.lower() and 'chimica' in text.lower().split():
					reply('Segui questo link per il programma di Chimica http://goo.gl/pVAp0o')
				if 'programm' in text.lower() and ( 'biochimica' in text.lower() or 'molecolare' in text.lower() ):
					reply('Ecco il programma di Biochimica parte1, parte2 e Biologia Molecolare http://goo.gl/ESNxAJ')
				if 'programm' in text.lower() and ( 'isto' in text.lower() or 'embrio' in text.lower() or 'citologia' in text.lower() ):
					reply('Segui questo link per il programma di Citologia, Istologia ed Embriologia http://goo.gl/NGG8XD')
				if 'programm' in text.lower() and ( 'metodologi' in text.lower() or 'semeiotica' in text.lower() ):
					reply('Segui questo link per il programma di Metodologie I anno http://goo.gl/wZ8Bqu e di Metodologia e Semeiotica Medico-Chirurgica III anno http://goo.gl/RnC35a')
				if 'programm' in text.lower() and 'micro' in text.lower():
					reply('Ecco il programma di microbiologia by Alfonso: http://goo.gl/4sJLdp')
				if 'programm' in text.lower() and 'anatomia' in text.lower() and not 'patologica' in text.lower():
					reply('Segui questo link per il programma di Anatomia http://goo.gl/CQgtfm')
				if 'sito' in text.lower() and ('saccia' in text.lower() or 'anatomia' in text.lower()):
					reply('Ecco il sito del Prof. Saccia:\nhttp://www.matsac.it/anatomia_1_med/')
				if 'programm' in text.lower() and 'fisiologia' in text.lower():
					reply('Segui questo link per il programma di Fisiologia http://goo.gl/JuOsvy')
				if 'programm' in text.lower() and ('patologia' in text.lower() or 'immunologia' in text.lower()):
					reply('Segui questo link per il programma di Patologia e Immunologia http://goo.gl/b9XbvI')
				if 'programm' in text.lower() and 'inglese' in text.lower():
					reply('Segui questo link per il programma di Inglese Scientifico http://goo.gl/FOH54g')
				if 'programm' in text.lower() and 'patologica' in text.lower():
					reply('Segui questo link per il programma di Anatomia Patologica I http://goo.gl/aIwm5L e Anatomia Patologica II http://goo.gl/JC8H7j')
				if 'programm' in text.lower() and 'laboratorio' in text.lower():
					reply('Segui questo link per il programma di Medicina di Laboratorio http://goo.gl/OqHaqK')
				if 'programm' in text.lower() and 'statistica' in text.lower():
					reply('Segui questo link per il programma di Statistica http://goo.gl/lvOfXO')
				if 'programm' in text.lower() and 'specialit' in text.lower():
					reply('Segui questo link per il programma di \n Specialità 1 http://goo.gl/n9ubqV \n Specialità 2 http://goo.gl/Y4GllY \n Specialità 3 http://goo.gl/y3Vus9 \n Specialità 4 http://goo.gl/TvZkPR \n Specialità 5 http://goo.gl/AQxrw6')
				if 'programm' in text.lower() and ('clinica' in text.lower() or 'organi' in text.lower() or 'senso' in text.lower()):
					reply('Segui questo link per il programma di Clinica Medico-Chirurgica degli Organi di Senso http://goo.gl/0EFv5k')
				if privacy == 'private':
					reply(fw='43591247')
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
