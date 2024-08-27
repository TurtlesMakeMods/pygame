import pygame
import time

# Button and Axis Mappings for Xbox 360 Controller
button_names = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
    4: "LB",
    5: "RB",
    6: "Back",
    7: "Start",
    8: "Left Stick Press",
    9: "Right Stick Press",
    10: "Xbox"
}

axis_names = {
    0: "Left Stick X",
    1: "Left Stick Y",
    2: "Right Stick X",
    3: "Right Stick Y",
    4: "Left Trigger",
    5: "Right Trigger"
}

# Deadzone threshold (ignore small joystick movements)
DEADZONE = 0.2

# Define refresh rates and labels
refresh_rates = [30, 60, 120]
refresh_rate_labels = ["Weak PC (30 FPS)", "Decent PC (60 FPS)", "Beefy PC (120 FPS)"]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
HIGHLIGHT = (255, 255, 0)

# Screen dimensions
WIDTH, HEIGHT = 800, 600

def apply_deadzone(value, deadzone=DEADZONE):
    """Apply deadzone handling to joystick axis values."""
    if abs(value) < deadzone:
        return 0
    return value

def draw_menu(screen, font, selected_option):
    """Draw the menu options on the screen."""
    screen.fill(BLACK)

    title_text = font.render("Select Refresh Rate", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    for i, label in enumerate(refresh_rate_labels):
        color = HIGHLIGHT if i == selected_option else WHITE
        option_text = font.render(label, True, color)
        screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 50))

    pygame.display.flip()

def controller_menu(screen, font):
    """Controller-based menu to select refresh rate using a graphical interface."""
    # Default refresh rate
    return 60
    """
    selected_option = 0
    draw_menu(screen, font, selected_option)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYHATMOTION:
                hat_x, hat_y = event.value
                if hat_y == 1:  # Up on the D-pad
                    selected_option = (selected_option - 1) % len(refresh_rates)
                    draw_menu(screen, font, selected_option)
                elif hat_y == -1:  # Down on the D-pad
                    selected_option = (selected_option + 1) % len(refresh_rates)
                    draw_menu(screen, font, selected_option)

            # Alternatively, use the Left Stick for navigation
            if event.type == pygame.JOYAXISMOTION:
                if event.axis in [1, 3]:  # Y-axis (Left/Right Stick)
                    value = apply_deadzone(event.value)
                    if value < -0.5:  # Up
                        selected_option = (selected_option - 1) % len(refresh_rates)
                        draw_menu(screen, font, selected_option)
                    elif value > 0.5:  # Down
                        selected_option = (selected_option + 1) % len(refresh_rates)
                        draw_menu(screen, font, selected_option)

            # Confirm selection with A Button
            if event.type == pygame.JOYBUTTONDOWN and event.button == 0:  # A button
                return refresh_rates[selected_option]

        pygame.time.wait(100)  # Delay to prevent overloading CPU during menu navigation
        """


def draw_controller_inputs(screen, font, button_events, axis_values, hat_values, controller_image):
    """Draw controller input events on the screen, over an Xbox 360 controller image."""
    screen.fill(BLACK)

    # Draw the controller image
    screen.blit(controller_image, (195, 290))  # Adjust the position if necessary

    # Display button events
    button_text = font.render("Buttons:", True, GREEN)
    screen.blit(button_text, (50, 100))
    for i, event in enumerate(button_events[-5:]):
        event_text = font.render(event, True, WHITE)
        screen.blit(event_text, (50, 130 + i * 30))

    # Display axis values
    axis_text = font.render("Axes:", True, GREEN)
    screen.blit(axis_text, (400, 100))
    for i, (axis_name, value) in enumerate(axis_values.items()):
        axis_event_text = font.render(f"{axis_name}: {value:.2f}", True, WHITE)
        screen.blit(axis_event_text, (400, 130 + i * 30))

    # Display D-pad (hat) values
    hat_text = font.render("D-pad:", True, GREEN)
    screen.blit(hat_text, (50, 300))
    hat_event_text = font.render(f"Position: {hat_values}", True, WHITE)
    screen.blit(hat_event_text, (50, 330))

    # Draw Quit Button
    quit_button_text = font.render("Quit", True, BLACK)
    quit_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 70, 100, 50)
    pygame.draw.rect(screen, GREEN, quit_button_rect)
    screen.blit(quit_button_text, (WIDTH // 2 - quit_button_text.get_width() // 2, HEIGHT - 60))

    pygame.display.flip()

def main():
    # Initialize pygame
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Controller Data Display Menu")

    # Load the font
    font = pygame.font.Font(None, 36)

    # Load the controller image
    controller_image = pygame.image.load('xbox360_controller.png')  # Add your image file path here

    # Initialize the joystick (controller)
    pygame.joystick.init()

    # Check if the controller is connected
    if pygame.joystick.get_count() == 0:
        print("No controller connected")
        exit()

    # Getting the controller
    controller = pygame.joystick.Joystick(0)
    controller.init()

    print(f"Controller name: {controller.get_name()}")

    # Set default refresh rate
    refresh_rate = 60

    clock = pygame.time.Clock()

    # Data storage for events
    button_events = []
    axis_values = {axis_name: 0.0 for axis_name in axis_names.values()}
    hat_values = (0, 0)

    # Main loop to check for controller inputs and display them on the screen
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                # Checks for button press and release events
                if event.type == pygame.JOYBUTTONDOWN:
                    button_name = button_names.get(event.button, f"Button {event.button}")
                    button_events.append(f"{button_name} pressed")
                    if len(button_events) > 5:  # Keep the last 5 events
                        button_events.pop(0)
                elif event.type == pygame.JOYBUTTONUP:
                    button_name = button_names.get(event.button, f"Button {event.button}")
                    button_events.append(f"{button_name} released")
                    if len(button_events) > 5:
                        button_events.pop(0)

                # Checks for joystick (analog stick) movement events
                if event.type == pygame.JOYAXISMOTION:
                    axis_name = axis_names.get(event.axis, f"Axis {event.axis}")
                    value = apply_deadzone(event.value)  # Apply deadzone
                    axis_values[axis_name] = value

                # Checks for D-pad (hat) movement events
                if event.type == pygame.JOYHATMOTION:
                    hat_values = event.value

            # Draw the updated inputs on the screen
            draw_controller_inputs(screen, font, button_events, axis_values, hat_values, controller_image)

            # Check for quit button click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            quit_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 70, 100, 50)
            if mouse_click[0] and quit_button_rect.collidepoint(mouse_x, mouse_y):
                return

            # Control the refresh rate
            clock.tick(refresh_rate)

    # Exit the loop if interrupted
    except KeyboardInterrupt:
        print("Exiting...")

    # Clean up resources
    finally:
        pygame.joystick.quit()
        pygame.quit()


if __name__ == "__main__":
    main()
