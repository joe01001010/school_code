import traceback

def draw_rectangle(**kwargs):
    width = kwargs.get('width', 0)
    height = kwargs.get('height', 0)
    symbol = kwargs.get('symbol', '*')
    try:
        if width <= 2 or height <= 2:
            raise ValueError("Width and height must be greater than 2.")
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("Symbol must be a single character string.")
        
        print(symbol * width)
        for i in range(height - 2):
            print(symbol + ' ' * (width - 2) + symbol)
        print(symbol * width)
    except:
        error_file = open('error_log.txt', 'a')
        error_file.write(traceback.format_exc())
        error_file.close()
        

def main():
    draw_rectangle(width=5, height=3, symbol='#')
    draw_rectangle(width=10, height=5, symbol='*')
    draw_rectangle(width=4, height=4, symbol='@')
    draw_rectangle(width=2, height=2)
    draw_rectangle(width=5, height=3, symbol='**')


if __name__ == "__main__":
    main()