"""
def handle_user_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state["is_window_open"] = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            state["is_blackout"] = True
            state["blackout_end_time"] = pygame.time.get_ticks() + 1000
        elif state["state"] != consts.RUNNING_STATE:
            continue
        elif event.type == pygame.MOUSEMOTION:
            rotate_arrow()
        elif event.type == pygame.MOUSEBUTTONDOWN and \
                not state["is_bubble_fired"] and \
                not state["bubbles_popping"]:
            fire_bubble()
            """