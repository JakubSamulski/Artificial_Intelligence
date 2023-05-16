problem_text="""Pralka zrzuca
wodę zaraz po jej
pobraniu.
""".replace('\n'," ")
reason_text = """Wąż spustowy jest na
nieodpowiedniej wysokości.
""".replace('\n'," ")
fix_text = """Podłącz wąż spustu wody tak, jak opisano
w instrukcji obsługi.
""".replace('\n',"")


text = f"""problem(pralka, "{problem_text}").\n
powod(pralka, "{problem_text}", "{reason_text}").\n
rozwiazanie(pralka, "{problem_text}","{reason_text}", "{fix_text}").
 """
print(text)