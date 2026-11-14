import os
import sys
import time
import msvcrt

class ProgressBarApp:
    def __init__(self):
        self.shirina = 40    
        self.protsent = 0
        self.bazovaya_zaderzhka = 0.05
        self.mnozhitel_skorosti = 1.0
        self.na_pauze = False

    def ochistka_ekrana(self):
        os.system('cls')

    def risovanie(self):
        zapolneno = int(self.shirina * self.protsent // 100)
        
        polosa = '█' * zapolneno + ' ' * (self.shirina - zapolneno)
        
        status = " [ПАУЗА]" if self.na_pauze else ""
        
        skorost_text = f" | Скорость: x{self.mnozhitel_skorosti:.1f}"
        
        vyvod = f"\rПрогресс: [{polosa}] {self.protsent}%{status}{skorost_text}" + " " * 15
        
        sys.stdout.write(vyvod)
        sys.stdout.flush()

    def obrabotka_vvoda(self):
        if msvcrt.kbhit():
            klavisha = msvcrt.getch()
            
            if klavisha == b'q' or klavisha == b'Q' or klavisha == b'\x1b': # q, Q или ESC
                return False
            elif klavisha == b' ':
                self.na_pauze = not self.na_pauze
            elif klavisha == b'r' or klavisha == b'R':
                self.protsent = 0
            elif klavisha == b'+' or klavisha == b'=': 
                self.mnozhitel_skorosti = round(min(10.0, self.mnozhitel_skorosti + 0.1), 1)
            elif klavisha == b'-' or klavisha == b'_':
                self.mnozhitel_skorosti = round(max(0.1, self.mnozhitel_skorosti - 0.1), 1)
                
        return True

    def obnovlenie_logiki(self):
        if not self.na_pauze:
            self.protsent += 1
            if self.protsent > 100:
                self.protsent = 0

    def zapusk(self):
        self.ochistka_ekrana()
        
        sys.stdout.write('\033[?25l')
        
        print("Управление:")
        print(" Пробел - Пауза/Продолжить")
        print(" + / - : Скорость")
        print(" r - Сброс на 0%")
        print(" q - Выход\n")

        try:
            rabotaem = True
            while rabotaem:
                rabotaem = self.obrabotka_vvoda()
                
                if not self.na_pauze:
                    self.obnovlenie_logiki()
                
                self.risovanie()
                
                realnaya_zaderzhka = self.bazovaya_zaderzhka / self.mnozhitel_skorosti
                time.sleep(realnaya_zaderzhka)
                
        except KeyboardInterrupt:
            pass 
        finally:
            sys.stdout.write('\033[?25h')
            self.ochistka_ekrana()
            print("Программа завершена.")

if __name__ == "__main__":
    app = ProgressBarApp()
    app.zapusk()