import uvage

camera = uvage.Camera(400,400)
box = uvage.from_color(300,300,"blue", 50,50)


def tick():
    # camera.draw(box)
    # camera.display()
    camera.clear("black")
    box.x += 1
    camera.draw(box)
    camera.display()


uvage.timer_loop(30,tick)