import pandas as pd

def get_subject_hours_for_class(cls_num, subjects):
    subject_hours = {}
    print(f"\nWprowadź liczbę godzin dla każdego przedmiotu w klasie {cls_num}:")
    for subject in subjects:
        while True:
            try:
                hours = int(input(f"{subject}: "))
                if hours < 0:
                    raise ValueError("Liczba godzin nie może być ujemna.")
                subject_hours[subject] = hours
                break
            except ValueError as e:
                print(f"Nieprawidłowa wartość: {e}. Spróbuj ponownie.")
    return subject_hours

def create_schedule(num_days, class_subject_hours):
    # Definiujemy przedmioty dodatkowe
    additional_subjects = [
        'REGULAMINY - PREGU', 'Wychowanie fizyczne', 'GDD', 
        '6 PROFILAKTYKA I DYSCYPLINA WOJSKOWA - PPIDW', '5 KSZTAŁCENIE OBYWATELSKIE - PKOBY',
        '14 ZARZĄDZANIE KRYZYSOWE - PZAKR', '24 PSERE', '30 OCHRONA ŚRODOWISKA - PŚROD ',
        '32 BEZPIECZEŃSTWO I HIGIENA PRACY - PBIHP','31 OCHRONA PPOŻ', '36 SZKOLENIE EKONIMICZNE - PEKON',
        '37 SZKOLENIE PRAWNE - PRAW', 'SZKOLENIE OGNIOWE - POGNI'
    ]
    
    # Inicjalizujemy plan lekcji
    schedule = {f'Klasa {i+1}': [['' for _ in range(7)] for _ in range(num_days)] for i in range(3)}
    
    # Zmienna do przechowywania ilości godzin dla każdego przedmiotu i klasy
    current_hours = {f'Klasa {i+1}': {subj: 0 for subj in list(class_subject_hours[i].keys()) + additional_subjects} for i in range(3)}
    
    # Maksymalna liczba lekcji w planie
    max_lessons = num_days * 7
    
    # Mapowanie godzin dla przedmiotów
    subject_time_slots = {}
    
    # Generowanie planu
    for day in range(num_days):
        for period in range(7):
            if (day % 4 == 0) and (period == 0):  # Co 4 dzień na 1. lekcji 'REGULAMINY - PREGU'
                for cls in range(3):
                    schedule[f'Klasa {cls+1}'][day][period] = 'REGULAMINY - PREGU'
                    current_hours[f'Klasa {cls+1}']['REGULAMINY - PREGU'] += 1
            elif (day % 2 == 0) and (period in [4, 5]):  # Co drugi dzień na 5. i 6. lekcji 'Wychowanie fizyczne'
                for cls in range(3):
                    schedule[f'Klasa {cls+1}'][day][period] = 'Wychowanie fizyczne'
                    current_hours[f'Klasa {cls+1}']['Wychowanie fizyczne'] += 1
            elif (day % 2 == 0) and (period == 6):  # Co drugi dzień na 7. lekcji, rozdzielamy te przedmioty zamiast 'wspólne'
                for cls in range(3):
                    for subject in ['6 PROFILAKTYKA I DYSCYPLINA WOJSKOWA - PPIDW', '5 KSZTAŁCENIE OBYWATELSKIE - PKOBY',
                                    '14 ZARZĄDZANIE KRYZYSOWE - PZAKR', '24 PSERE', '30 OCHRONA ŚRODOWISKA - PŚROD ',
                                    '32 BEZPIECZEŃSTWO I HIGIENA PRACY - PBIHP', '31 OCHRONA PPOŻ','36 SZKOLENIE EKONIMICZNE - PEKON',
                                    '37 SZKOLENIE PRAWNE - PRAW']:
                        if current_hours[f'Klasa {cls+1}'][subject] < class_subject_hours[cls][subject]:
                            schedule[f'Klasa {cls+1}'][day][period] = subject
                            current_hours[f'Klasa {cls+1}'][subject] += 1
                            break
            elif day == 3:  # W 4 dzień lekcji 'SZKOLENIE OGNIOWE - POGNI'
                for cls in range(3):
                    schedule[f'Klasa {cls+1}'][day][period] = 'SZKOLENIE OGNIOWE - POGNI'
                    current_hours[f'Klasa {cls+1}']['SZKOLENIE OGNIOWE - POGNI'] += 1
            #elif (day == 0 and period in [1, 2, 3]) or (day == 4 and period in [1, 2, 3]) or (day == 8 and period in [1, 2, 3]):  # Co 1,4,8 dzień na 1. i 2,3. lekcji 'GDD' można modyfikowac 
             #   for cls in range(3):
              #      for subject in ['GDD']:
               #         if current_hours[f'Klasa {cls+1}'][subject] < class_subject_hours[cls][subject]:
                #            schedule[f'Klasa {cls+1}'][day][period] = subject
                 #           current_hours[f'Klasa {cls+1}'][subject] += 1
                  #          break
            else:
                for cls in range(3):
                    if sum(current_hours[f'Klasa {cls+1}'].values()) < max_lessons:
                        placed = False
                        for subject in class_subject_hours[cls].keys():
                            if subject != 'SZKOLENIE OGNIOWE - POGNI' and current_hours[f'Klasa {cls+1}'][subject] < class_subject_hours[cls][subject]:
                                # Sprawdzamy, czy przedmiot już ma przypisane godziny w tej lekcji
                                if subject in subject_time_slots and subject_time_slots[subject][day][period] != '':
                                    schedule[f'Klasa {cls+1}'][day][period] = subject_time_slots[subject][day][period]
                                else:
                                    schedule[f'Klasa {cls+1}'][day][period] = subject
                                    subject_time_slots.setdefault(subject, [['' for _ in range(7)] for _ in range(num_days)])[day][period] = subject
                                current_hours[f'Klasa {cls+1}'][subject] += 1
                                placed = True
                                break
                        if not placed:
                            schedule[f'Klasa {cls+1}'][day][period] = 'wolne'
    
    # Sprawdzamy nadmiar godzin i godziny nieprzydzielone
    excess_hours = {f'Klasa {i+1}': {} for i in range(3)}
    unassigned_hours = {f'Klasa {i+1}': {subj: 0 for subj in class_subject_hours[i].keys()} for i in range(3)}
    
    for cls in range(3):
        for subj, hours in class_subject_hours[cls].items():
            assigned_hours = current_hours[f'Klasa {cls+1}'].get(subj, 0)
            if hours > assigned_hours:
                unassigned_hours[f'Klasa {cls+1}'][subj] = hours - assigned_hours
            elif hours < assigned_hours:
                excess_hours[f'Klasa {cls+1}'][subj] = assigned_hours - hours
    
    return schedule, excess_hours, unassigned_hours 

def print_schedule(schedule, excess_hours, unassigned_hours):
    # Wyświetlanie planu lekcji
    for day in range(len(schedule['Klasa 1'])):
        print(f"\nDzień {day + 1}:")
        for period in range(7):
            period_str = f" Godzina {period + 1}: "
            period_schedule = [schedule[f'Klasa {cls+1}'][day][period].ljust(20) for cls in range(3)]
            print(period_str + " | ".join(period_schedule))
    
    # Wyświetlanie nadmiaru godzin
    print("\nNadmiar godzin:")
    for cls in excess_hours:
        if excess_hours[cls]:
            print(f"\n{cls}:")
            for subj, hours in excess_hours[cls].items():
                print(f"{subj}: {hours} godz.")
        else:
            print(f"\n{cls}: Brak nadmiaru godzin")
    
    # Wyświetlanie nieprzydzielonych godzin
    print("\nNieprzydzielone godziny:")
    for cls in unassigned_hours:
        if unassigned_hours[cls]:
            print(f"\n{cls}:")
            for subj, hours in unassigned_hours[cls].items():
                print(f"{subj}: {hours} godz.")
        else:
            print(f"\n{cls}: Brak nieprzydzielonych godzin")


if __name__ == "__main__":
    num_days = int(input("Podaj liczbę dni: "))
    subjects_class_1 = [
          'SZKOLENIE OGNIOWE - POGNI',
        '38 SYSTEM WYKORZYSTYWANIA DOŚWIADCZEŃ - PSWDO', '40 OCENA STOPNIA WYSZKOLENIA', 
        '15 PRZPOZNANIE I ARMIE INNYCH PAŃSTW I WRE - PRAIP', '16 SZKOLENIE INŻYNIERYJNO-SAPERSKIE - PINŻS', '17 OBRONA PRZED BRONIĄ MASOWEGO RAŻENIA - POPBM',
        '18 POWSZECHNA OBRONA - PPOPL', '20 TERENOZNASTWO - PTERE','23 SZKOLENIE MEDYCZNE - PMED','8 TAKTYKA 1 - PTAKT 1','10 TAKTYKA ŁĄCZNOŚCI - PTAKŁ', '21 OCHRONA I OBRONA OBIEKTÓW - POIOO', 
        '26 UŻYTKOWANIE SPRZET ŁĄCZNOŚCI - PUSŁĄ', '34 OBSŁUGIWANIE SPRZETU','28 BUDOWA I EKSPLOATACJA SPW - PIBES','35 EKSPLOATACJA W POLOWYCH 1 - PEKSP 1', '27 SZKOL DOSKONALĄCE NA STANOWISKACH - PSDNS','19 ŁĄCZNOŚĆ 1 - PŁĄCZ 1', 'GDD', '6 PROFILAKTYKA I DYSCYPLINA WOJSKOWA - PPIDW','5 KSZTAŁCENIE OBYWATELSKIE - PKOBY','14 ZARZĄDZANIE KRYZYSOWE - PZAKR', '24 PSERE',
        '30 OCHRONA ŚRODOWISKA - PŚROD ', '32 BEZPIECZEŃSTWO I HIGIENA PRACY - PBIHP','31 OCHRONA PPOŻ', '36 SZKOLENIE EKONIMICZNE - PEKON', '37 SZKOLENIE PRAWNE - PRAW'
    ]
    subjects_class_2 = [     
         'SZKOLENIE OGNIOWE - POGNI',
        '38 SYSTEM WYKORZYSTYWANIA DOŚWIADCZEŃ - PSWDO', '40 OCENA STOPNIA WYSZKOLENIA', 
        '15 PRZPOZNANIE I ARMIE INNYCH PAŃSTW I WRE - PRAIP', '16 SZKOLENIE INŻYNIERYJNO-SAPERSKIE - PINŻS', '17 OBRONA PRZED BRONIĄ MASOWEGO RAŻENIA - POPBM',
        '18 POWSZECHNA OBRONA - PPOPL', '20 TERENOZNASTWO - PTERE','23 SZKOLENIE MEDYCZNE - PMED', '11 SZKOLENIE TAKTYCZNO SPECIALNE - PTAKS','21 OCHRONA I OBRONA OBIEKTÓW - POIOO',  '28 BUDOWA I EKSPLOATACJA SPW - PIBES',
        '33 OBSŁUGIWANIE TECHNICZNE SPW - POBTE',  '27 SZKOL DOSKONALĄCE NA STANOWISKACH - PSDNS','19 ŁĄCZNOŚĆ 2 - PŁĄCZ', 'GDD','6 PROFILAKTYKA I DYSCYPLINA WOJSKOWA - PPIDW','5 KSZTAŁCENIE OBYWATELSKIE - PKOBY','14 ZARZĄDZANIE KRYZYSOWE - PZAKR', '24 PSERE',
        '30 OCHRONA ŚRODOWISKA - PŚROD ', '32 BEZPIECZEŃSTWO I HIGIENA PRACY - PBIHP','31 OCHRONA PPOŻ', '36 SZKOLENIE EKONIMICZNE - PEKON', '37 SZKOLENIE PRAWNE - PRAW'
    ]
    subjects_class_3 = [
         'SZKOLENIE OGNIOWE - POGNI', '40 OCENA STOPNIA WYSZKOLENIA', 
        '15 PRZPOZNANIE I ARMIE INNYCH PAŃSTW I WRE - PRAIP', '16 SZKOLENIE INŻYNIERYJNO-SAPERSKIE - PINŻS', '17 OBRONA PRZED BRONIĄ MASOWEGO RAŻENIA - POPBM',
        '18 POWSZECHNA OBRONA - PPOPL', '20 TERENOZNASTWO - PTERE','23 SZKOLENIE MEDYCZNE - PMED','8 TAKTYKA 3 - PTAKT','12 TAKTYKA W CHEMICZNYCH - PCHEM', '21 OCHRONA I OBRONA OBIEKTÓW - POIOO', 
        '28 BUDOWA I EKSPLOATACJA SPW - PBIES', '34 OBSŁUGA SPRZETU 3 - POBSP', '19 ŁĄCZNOŚĆ 3 - PŁĄCZ', '9 SZKOLENIE RATOWNICZE', 'GDD','6 PROFILAKTYKA I DYSCYPLINA WOJSKOWA - PPIDW', '5 KSZTAŁCENIE OBYWATELSKIE - PKOBY','14 ZARZĄDZANIE KRYZYSOWE - PZAKR', '24 PSERE',
        '30 OCHRONA ŚRODOWISKA - PŚROD ', '32 BEZPIECZEŃSTWO I HIGIENA PRACY - PBIHP','31 OCHRONA PPOŻ', '36 SZKOLENIE EKONIMICZNE - PEKON', '37 SZKOLENIE PRAWNE - PRAW'
    ]
    # Pobieranie godzin dla każdego przedmiotu w klasie
    class_subject_hours = [
        get_subject_hours_for_class(1, subjects_class_1),
        get_subject_hours_for_class(2, subjects_class_2),
        get_subject_hours_for_class(3, subjects_class_3)
    ]
    
    schedule, excess_hours, unassigned_hours = create_schedule(num_days, class_subject_hours)
    print_schedule(schedule, excess_hours, unassigned_hours)
