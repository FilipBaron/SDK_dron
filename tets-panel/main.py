from nicegui import ui

with ui.column().classes('w-full'):

    with ui.row().classes('w-full items-center justify-between flex-nowrap'):

        with ui.column().classes('gap-1'):
            ui.button('UP', color='secondary').classes('w-14 h-14')
            ui.button('DWN', color='secondary').classes('w-14 h-14')

        with ui.column().classes('flex-1 items-center'):
            ui.image('https://dummyimage.com/640x480/2a2a2a/ffffff.png&text=Camera+Stream').classes('w-full object-contain')

        with ui.grid(columns=3).classes('gap-1'):
            ui.label()
            ui.button('FWD').classes('w-14 h-14')
            ui.label()

            ui.button('LFT').classes('w-14 h-14')
            ui.button('STP', color='red').classes('w-14 h-14')
            ui.button('RGT').classes('w-14 h-14')

            ui.label()
            ui.button('BWD').classes('w-14 h-14')
            ui.label()

    with ui.card().classes('w-full'):
        ui.label('Telemetry').classes('font-bold')

        with ui.row().classes('w-full flex-wrap'):
            ui.label('Status: CONNECTED')
            ui.label('Battery: 87%')
            ui.label('Altitude: 14.2 m')
            ui.label('Speed: 2.1 m/s')
            ui.label('Pitch: 1.5°')
            ui.label('Roll: -0.2°')
            ui.label('Yaw: 274°')


ui.run(host='0.0.0.0', port=8080)
