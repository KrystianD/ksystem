devices_variants = {
    "attiny1626": {
        "usarts": {
            "USART0": {
                "pinout": [
                    {
                        "pin_tx": "B2",
                        "pin_rx": "B3",
                        "pin_xdir": "B0",
                        "setup_code": "",
                    },
                    {
                        "pin_tx": "A1",
                        "pin_rx": "A2",
                        "pin_xdir": "A4",
                        "setup_code": "PORTMUX.USARTROUTEA |= PORTMUX_USART0_ALT1_gc",
                    },
                ]
            },
            "USART1": {
                "pinout": [
                    {
                        "pin_tx": "A1",
                        "pin_rx": "A2",
                        "pin_xdir": "A4",
                        "setup_code": "",
                    },
                    {
                        "pin_tx": "C2",
                        "pin_rx": "C1",
                        "pin_xdir": "C3",
                        "setup_code": "PORTMUX.USARTROUTEA |= PORTMUX_USART1_ALT1_gc",
                    },
                ]
            },
        },
    },
    "attiny414": {
        "usarts": ["USART0"],
    },
}
