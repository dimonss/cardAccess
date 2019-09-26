import pygame
import pygame as pg
from box import InputBox

import  psycopg2
import pyttsx3
import datetime

def speak(what):
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

con = psycopg2.connect(
        host = "localhost",
        database = "cardDB",
        user = "postgres",
        password = "1722",
        port = 5432)

cur = con.cursor()

speak_engine = pyttsx3.init()


pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 200, 140, 32)
    input_box3 = InputBox(100, 300, 140, 32)
    input_box4 = InputBox(100, 400, 140, 32)
    input_boxes = [input_box1, input_box2, input_box3, input_box4]
    done = False

    status = True
    while not done:
        for event in pg.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_RETURN:
                    try:
                        text = str(input_box1.text)
                        if text != "":
                            now = datetime.datetime.now()
                            date = str(now.year) + '  ' + str(now.month) + '  ' + str(now.day) + '  ' + str(now.hour) + ":" + str(now.minute)
                            # cur.execute('INSERT INTO "info_card" (id_card, name_employees) VALUES ('+"'"+text+"'"+", 'один');")
                            print('INSERT INTO "actions" (id_card, entering, time_pass) VALUES ('
                                        +"'"+str(text)+"' , "+str(status)+", '"+date+"');")
                            cur.execute('INSERT INTO "actions" (id_card, entering, time_pass) VALUES ('
                                        +"'"+str(text)+"' , "+str(status)+", '"+date+"');")
                            print("SELECT name_employees from info_card WHERE id_card='"+text+"';")
                            cur.execute("SELECT name_employees from info_card WHERE id_card='"+text+"';")
                            name = cur.fetchall()
                            print("3")
                            print("SELECT name_employees from info_card WHERE id_card='"+text+"';")
                            if status == True:
                                speak('Здраствуйте'+str(name))
                            else:
                                speak('Досвидание'+str(name))
                            status = not status
                            input_box1.text = ""

                            print(date)
                            con.commit()
                    except:
                        print("error")
            if event.type == pygame.QUIT:
                exit()
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()