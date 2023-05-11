from dotenv import load_dotenv, dotenv_values
from colorist import Color

load_dotenv()
config = dotenv_values(".env")
THRESHOLD = 0.05

def output_p_values(p_test_values: list):
    print(f"{Color.YELLOW}Leading 20 Ascending ...{Color.OFF} \n")
    for i, p_test in enumerate(p_test_values[:20]):
            if p_test['p-value'] <= THRESHOLD:
                print(f"{Color.YELLOW}{p_test['pair']['a']} - {p_test['pair']['b']}:{Color.OFF}{Color.CYAN} {p_test['p-value']}{Color.OFF} - {Color.GREEN}✔️ PASS{Color.OFF}")
            else:
                print(f"{Color.YELLOW}{p_test['pair']['a']} - {p_test['pair']['b']}:{Color.OFF}{Color.CYAN} {p_test['p-value']}{Color.OFF} - {Color.RED}❌ FAIL{Color.OFF}")
