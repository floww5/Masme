# testing aja

impor mekanis
permintaan impor
impor ulang
impor logging
impor argparse
impor sys

memuat ulang (sys)
sys.setdefaultencoding ('utf8')

kelas buat:
    def __init __ (mandiri):
        logging.basicConfig (
            level = {
                Benar: logging. Debug,
                Salah: logging.INFO
            } [arg.level],
            format = '\ r% (levelname) s:% (nama) s:% (pesan) s'
        )
        self.create_total = 0
        self.blacklist_email = [] # '@ datasetoma', '@geroev', '@cliptik', '@khtyler', '@ parcel4']
        self.temp_email_url = 'https://tempmail.net'

        diri .__ utama __ ()

    def _browser_options (mandiri):
        br = mechanize.Browser ()
        br.set_handle_robots (False)
        br.set_handle_equiv (Benar)
        br.set_handle_referer (Benar)
        br.set_handle_redirect (Benar)
        jika arg.proxy:
            br.set_proxies ({"http": arg.proxy,
                            "https": arg.proxy,
                            })
        br.set_handle_refresh (
            mechanize._http.HTTPRefreshProcessor (),
            max_time = 5
        )
        br.addheaders = [('Agen-pengguna', "Mozilla / 5.0 (Linux; Android 5.0; ASUS_T00G Build / LRX21V) AppleWebKit / 537.36 (KHTML, seperti Gecko) Chrome / 61.0.3163.98 Mobile Safari / 537.36")]

        kembali br

    # info akun
    def _get_info_account (mandiri):
        logging.info ('mencari informasi akun')
        res = requests.get ('https://randomuser.me/api') .json ()

        pwd = res ['results'] [0] ['login'] ['password']
        kembali {
            'username': res ['results'] [0] ['login'] ['username'],
            'kata sandi': pwd + '-zvtyrdt.id' jika len (pwd) <6 lain pwd,
            'firstname': res ['results'] [0] ['name'] ['first'],
            'nama belakang': res ['hasil'] [0] ['nama'] ['akhir'],
            'gender': '1' jika res ['results'] [0] ['gender'] == 'female' else '2',
            'date': res ['results'] [0] ['dob'] ['date']. split ('T') [0] .split ('-')
        }

    # facebook
    def _create_account_facebook (mandiri, email):
        data = self._get_info_account ()

        self._password = data ['kata sandi']
        logging.info ('nama:% s', data ['firstname'] + '' + data ['lastname'])
        logging.info ('buat akun facebook')
        self.br.open ('https://mbasic.facebook.com/reg/?cid=102&refid=8')

        self.br.select_form (nr = 0)
        self.br.form ['firstname'] = data ['firstname'] + '' + data ['lastname']
        mencoba:
            self.br.form ['reg_email__'] = email
        kecuali mechanize._form_controls.ControlNotFoundError sebagai contoh:
            logging.warning (str (ex))
            mengembalikan False

        self.br.form ['sex'] = [data ['gender']]
        self.br.form ['birthday_day'] = [data ['date'] [2] [1:] jika data ['date'] [2] [0] == '0' data lain ['date'] [2]]
        self.br.form ['birthday_month'] = [data ['date'] [1] [1:] jika data ['date'] [1] [0] == '0' data lain ['date'] [1]]
        self.br.form ['birthday_year'] = [data ['date'] [0]]
        self.br.form ['reg_passwd__'] = data ['kata sandi']
        self.br.submit ()

        jika "captcha" di self.br.response (). read (). lower ():
            sys.exit (logging.error ("Anda kedapatan membuat akun palsu dan pengguna spam. maaf, coba lagi besok ... ok bye bye \ n"))
        untuk saya dalam kisaran (3):
            self.br.select_form (nr = 0)
            self.br.submit ()

        gagal = re.findall (r'id = "registrasi-kesalahan"> <div class = "bl"> (. +?) <', self.br.response (). read ())
        jika gagal:
            logging.error (gagal [0])
            mengembalikan False
        mengembalikan True

    def _check_email_fb (mandiri, email):
        self.br.open ('https://mbasic.facebook.com/login/identify')
        self.br._factory.is_html = Benar
        self.br.select_form (nr = 0)
        self.br.form ['email'] = email
        self.br.submit ()

        jika "recover_method" di self.br.response (). read ():
            logging.info ("ambil alih akun")
            self.br._factory.is_html = Benar
            self.br.select_form (nr = 0)
            self.br.form ['recover_method'] = ['send_email']
            self.br.submit ()
            mengembalikan False

        mengembalikan True

    def _submit_code (mandiri, kode):
        self.br._factory.is_html = Benar
        self.br.select_form (nr = 0)
        self.br.form ['n'] = kode
        self.br.submit ()

    def _change_password (mandiri):
        data = self._get_info_account ()
        self._password = data ['kata sandi']

        self.br._factory.is_html = Benar
        self.br.select_form (nr = 0)
        self.br.form ['password_new'] = self._password
        self.br.submit ()

    # surat
    def _open_temp_mail (mandiri):
        return self.br.open (self.temp_email_url) .read ()

    def _find_email (mandiri, teks):
        return re.findall (r'value = "(. + @. +)" ', teks) [0]

    def _read_message (mandiri, teks):
        x = re.findall (r'baslik "> (\ d +) \ s ', teks)
        jika x:
            logging.info ("kode Anda:% s"% x [0])
            mengembalikan True

    def _save_to_file (mandiri, email, kata sandi):
        dengan open ('akun.txt', 'a') sebagai f:
            f.write ('% s |% s \ n'% (email, kata sandi))

    def __main __ (mandiri):
        sementara Benar:
            self.br = self._browser_options ()
            logging.info ('mencari email baru')

            email_found, periksa, max_ = Salah, Benar, 0
            sementara Benar:
                res_em = self._open_temp_mail ()
                self._mail = self._find_email (res_em)

                jika '@' + self._mail.split ('@') [1] .split ('.') [0] di self.blacklist_email:
                    logging.error ('email daftar hitam:% s', self._mail)
                    istirahat

                jika tidak email_found:
                    logging.info ('email yang diperoleh:% s', self._mail)
                    jika self._check_email_fb (self._mail):
                        jika self._create_account_facebook (self._mail):
                            email_found = Benar
                    lain:
                        logging.info ('menunggu email masuk')
                        code = self._read_message (res_em)
                        jika kode:
                            self._submit_code (kode)

                jika max_ == 10:
                    logging.error ('tidak ada respons!')
                    istirahat
                jika periksa dan email_found:
                    self.create_total + = 1
                    logging.info ('akun dibuat: \ n \ t email:% s \ n \ t kata sandi:% s', self._mail, self._password)
                    self._save_to_file (self._mail, self._password)
                    check = Salah
                    max_ + = 1
                lain: istirahat

            jika self.create_total == arg.count:
                logging.info ('selesai \ n')
                istirahat

if __name__ == '__main__':
    parse = argparse.ArgumentParser ()
    parse.add_argument ('-c', metavar = '<COUNT>', ketik = int, dest = 'count',
        help = 'jumlah akun yang ingin Anda buat')
    parse.add_argument ('-p', metavar = '<IP: PORT>', dest = 'proxy',
        help = 'set proxy')
    parse.add_argument ('- debug', action = 'store_true', dest = 'level',
        help = 'atur level logging ke debug')
    arg = parse.parse_args ()

    jika arg.count:
        mencoba:
            cetak ('') # baris baru
            membuat()
        kecuali KeyboardInterrupt:
            logging.error ('interupsi pengguna .. \ n')
# kecuali Pengecualian sebagai pengecualian:
 # logging.critical (str (exc) + '\ n')
    lain:
        parse.print_help ()
