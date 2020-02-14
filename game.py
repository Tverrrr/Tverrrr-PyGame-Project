import pygame
from pygame.sprite import Sprite
import os
import csv
import random

green = (153, 255, 153)
yellow = (153, 153, 255)
dBlue = (73, 96, 117)
lBlue = (194, 241, 219)
black = (0, 0, 0)
white = (255, 255, 255)
orange = (243, 192, 128)
purple = (85, 90, 96)

help = {1: 0, 2: 0, 3: 0, 4: 0}

pygame.init()
clock = pygame.time.Clock()
timeCounter = 0
window = pygame.display.set_mode((950, 600))
pygame.display.set_caption("Cookie Clicker")
window.fill(orange)
autoCPSMenuVisible = False
upgradeMenuVisible = False

cookieImage = pygame.image.load(os.path.join("Картинки", "cookie.png"))
grandMotherImage = pygame.image.load(os.path.join("Картинки", "woman.png"))
farmImage = pygame.image.load(os.path.join("Картинки", "food.png"))
mineImage = pygame.image.load(os.path.join("Картинки", "wagon.png"))
factoryImage = pygame.image.load(os.path.join("Картинки", "factory.png"))
bankImage = pygame.image.load(os.path.join("Картинки", "bank.png"))
cursorUpgradeImage = pygame.image.load(os.path.join("Картинки", "click.png"))
grandMotherUpgradeImage = pygame.image.load(os.path.join("Картинки", "womanUpgrade.png"))
farmUpgradeImage = pygame.image.load(os.path.join("Картинки", "foodUpgrade.png"))
mineUpgradeImage = pygame.image.load(os.path.join("Картинки", "wagonUpgrade.png"))
factoryUpgradeImage = pygame.image.load(os.path.join("Картинки", "factoryUpgrade.png"))
all_sprites = pygame.sprite.Group()

if os.path.exists("config.csv"):
    data = []
    with open("config.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for index, row in enumerate(reader):
            data.append(row)
        print(len(data[0]), len(data[1]))
        for i in range(len(data[0])):
            exec("{} = int({})".format(data[0][i], data[1][i]))
else:
    pass


def countCPS():
    nCPS = 0
    nCPS += grandMotherCPS.owned * (2 ** grandMotherUpgrade.level)
    nCPS += farmsCPS.owned * 10 * (2 ** farmUpgrade.level)
    nCPS += minesCPS.owned * 100 * (2 ** mineUpgrade.level)
    nCPS += factoryCPS.owned * 1000 * (2 ** factoryUpgrade.level)
    nCPS += 10000 * banksCPS.owned
    return nCPS


class Cookie(Sprite):
    def __init__(self, x, y, var, cook):
        self.x = x
        self.y = y
        self.var = var
        self.font = pygame.font.Font(r"C:\Windows\Fonts\REFSAN.TTF", 40)
        self.COOKIES = cook
        self.rect = cookieImage.get_rect(center=(self.x, self.y))

    def draw(self):
        window.fill(orange)
        window.blit(cookieImage, self.rect)

        commaCookieCount = "{} печенек".format(int(self.COOKIES))
        cookieCountDisplay = self.font.render(commaCookieCount, True, purple)
        text_rect = cookieCountDisplay.get_rect(center=(475, 50))
        window.blit(cookieCountDisplay, text_rect)

        CPStext = self.font.render(str(countCPS()) + " печенек в секунду", True, purple)
        CPStextRect = CPStext.get_rect(center=(475, 130))
        window.blit(CPStext, CPStextRect)


def drawSaveButton():
    buttonFont = pygame.font.Font(r"C:\Windows\Fonts\REFSAN.TTF", 40)
    saveText = buttonFont.render("СОХРАНИТЬ", True, purple)
    drawSaveButton.saveButtonRect = saveText.get_rect(center=(485, 565))
    pygame.draw.rect(window, purple, drawSaveButton.saveButtonRect, 5)
    window.blit(saveText, drawSaveButton.saveButtonRect)


def drawMenuButtons():
    buttonFont = pygame.font.Font(r"C:\Windows\Fonts\REFSAN.TTF", 40)

    autoCPSButtonText = buttonFont.render("АВТО CPS", True, purple)
    drawMenuButtons.autoCPSButtonRect = autoCPSButtonText.get_rect(center=(200, 565))
    pygame.draw.rect(window, purple, drawMenuButtons.autoCPSButtonRect, 5)
    window.blit(autoCPSButtonText, drawMenuButtons.autoCPSButtonRect)

    upgradeButtonText = buttonFont.render("АПГРЕЙД", True, purple)
    drawMenuButtons.upgradeButtonRect = upgradeButtonText.get_rect(center=(755, 565))
    pygame.draw.rect(window, purple, drawMenuButtons.upgradeButtonRect, 5)
    window.blit(upgradeButtonText, drawMenuButtons.upgradeButtonRect)


def drawMenus():
    lockedFont = pygame.font.Font(r"C:\Windows\Fonts\REFSAN.TTF", 40)
    lockedText = lockedFont.render("?????????????", True, purple)

    lockedAutoCPS = {"Rect1": lockedText.get_rect(center=(200, 170)),
                     "Rect2": lockedText.get_rect(center=(200, 270)),
                     "Rect3": lockedText.get_rect(center=(200, 370)),
                     "Rect4": lockedText.get_rect(center=(200, 470))}

    lockedAutoCPSOutlines = {"Outline1": pygame.Rect((25, 220), (350, 100)),
                             "Outline2": pygame.Rect((25, 320), (350, 100)),
                             "Outline3": pygame.Rect((25, 420), (350, 100))}

    autoCPSRect = pygame.Rect((25, 20), (350, 500))

    if autoCPSMenuVisible:
        pygame.draw.rect(window, orange, autoCPSRect)
        pygame.draw.rect(window, purple, autoCPSRect, 5)
        if UNLOCKED_AUTOCPS == 1:
            window.blit(lockedText, lockedAutoCPS["Rect1"])
            window.blit(lockedText, lockedAutoCPS["Rect2"])
            window.blit(lockedText, lockedAutoCPS["Rect3"])
            window.blit(lockedText, lockedAutoCPS["Rect4"])
            pygame.draw.rect(window, purple, lockedAutoCPSOutlines["Outline1"], 5)
            pygame.draw.rect(window, purple, lockedAutoCPSOutlines["Outline2"], 5)
            pygame.draw.rect(window, purple, lockedAutoCPSOutlines["Outline3"], 5)
        elif UNLOCKED_AUTOCPS == 2:
            window.blit(lockedText, lockedAutoCPS["Rect2"])
            window.blit(lockedText, lockedAutoCPS["Rect3"])
            window.blit(lockedText, lockedAutoCPS["Rect4"])
            pygame.draw.rect(window, purple, lockedAutoCPSOutlines["Outline2"], 5)
            pygame.draw.rect(window, purple, lockedAutoCPSOutlines["Outline3"], 5)
        elif UNLOCKED_AUTOCPS == 3:
            window.blit(lockedText, lockedAutoCPS["Rect3"])
            window.blit(lockedText, lockedAutoCPS["Rect4"])
            pygame.draw.rect(window, purple, lockedAutoCPSOutlines["Outline3"], 5)
        elif UNLOCKED_AUTOCPS == 4:
            window.blit(lockedText, lockedAutoCPS["Rect4"])

    lockedUpgrades = {"Rect1": lockedText.get_rect(center=(755, 170)),
                     "Rect2": lockedText.get_rect(center=(755, 270)),
                     "Rect3": lockedText.get_rect(center=(755, 370)),
                     "Rect4": lockedText.get_rect(center=(755, 470))}

    lockedUpgradesOutlines = {"Outline1": pygame.Rect((573, 220), (350, 100)),
                             "Outline2": pygame.Rect((573, 320), (350, 100)),
                             "Outline3": pygame.Rect((573, 420), (350, 100))}

    autoCPSRect = pygame.Rect((573, 20), (350, 500))

    if upgradeMenuVisible:
        pygame.draw.rect(window, orange, autoCPSRect)
        pygame.draw.rect(window, purple, autoCPSRect, 5)
        if UNLOCKED_UPGRADES == 1:
            window.blit(lockedText, lockedUpgrades["Rect1"])
            window.blit(lockedText, lockedUpgrades["Rect2"])
            window.blit(lockedText, lockedUpgrades["Rect3"])
            window.blit(lockedText, lockedUpgrades["Rect4"])
            pygame.draw.rect(window, purple, lockedUpgradesOutlines["Outline1"], 5)
            pygame.draw.rect(window, purple, lockedUpgradesOutlines["Outline2"], 5)
            pygame.draw.rect(window, purple, lockedUpgradesOutlines["Outline3"], 5)
        elif UNLOCKED_UPGRADES == 2:
            window.blit(lockedText, lockedUpgrades["Rect2"])
            window.blit(lockedText, lockedUpgrades["Rect3"])
            window.blit(lockedText, lockedUpgrades["Rect4"])
            pygame.draw.rect(window, purple, lockedUpgradesOutlines["Outline2"], 5)
            pygame.draw.rect(window, purple, lockedUpgradesOutlines["Outline3"], 5)
        elif UNLOCKED_UPGRADES == 3:
            window.blit(lockedText, lockedUpgrades["Rect3"])
            window.blit(lockedText, lockedUpgrades["Rect4"])
            pygame.draw.rect(window, purple, lockedUpgradesOutlines["Outline3"], 5)
        elif UNLOCKED_UPGRADES == 4:
            window.blit(lockedText, lockedUpgrades["Rect4"])


class Upgrade:
    def __init__(self, image, title, description, level, price, number, cursor=False):
        self.image = image
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.title = title
        self.description = description
        self.level = level
        self.price = price
        self.number = number
        self.cursor = cursor
        self.upgradeFonts = {"titleFont": pygame.font.Font(r"C:\Windows\Fonts\REFSAN.TTF", 26),
                             "descFont": pygame.font.Font(r"C:\Windows\Fonts\REFSAN.TTF", 17),
                             "levelFont": pygame.font.Font(r"C:\Windows\Fonts\REFSAN.TTF", 24)}
        self.outline = pygame.Rect((573, (self.number - 1) * 100 + 20), (350, 100))
        self.titleText = self.upgradeFonts["titleFont"].render(self.title, True, purple)
        self.descText = self.upgradeFonts["descFont"].render(self.description, True, purple)
        self.titleRect = self.titleText.get_rect(center=(760, (self.number - 1) * 100 + 35))
        self.imageRect = self.image.get_rect(center=(605, (self.number - 1) * 100 + 55))
        self.descRect = self.descText.get_rect(center=(760, (self.number - 1) * 100 + 55))
        self.draw()

    def draw(self):
        self.levelText = self.upgradeFonts["levelFont"].render("УРОВЕНЬ {}".format(self.level), True, purple)
        self.buyText = self.upgradeFonts["levelFont"].render("ЦЕНА {}".format(self.price), True, purple)
        self.powerText = self.upgradeFonts["levelFont"].render("МОЩНОСТЬ {}".format(CURSOR_POWER), True, purple)
        self.levelRect = self.levelText.get_rect(center=(835, (self.number - 1) * 100 + 105))
        self.buyRect = self.image.get_rect(center=(610, (self.number - 1) * 100 + 123))
        self.powerRect = self.descText.get_rect(center=(800, (self.number - 1) * 100 + 80))

        if upgradeMenuVisible:
            if self.number <= UNLOCKED_UPGRADES:
                pygame.draw.rect(window, purple, self.outline, 5)
                window.blit(self.image, self.imageRect)
                window.blit(self.titleText, self.titleRect)
                window.blit(self.descText, self.descRect)
                window.blit(self.levelText, self.levelRect)
                window.blit(self.buyText, self.buyRect)
                if self.cursor:
                    window.blit(self.powerText, self.powerRect)


class AutoCPS:
    def __init__(self, image, title, description, cps, owned, ownedInfo, price, basePrice, number):
        self.image = image
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.title = title
        self.description = description
        self.cps = cps
        self.owned = owned
        self.ownedInfo = ownedInfo
        self.price = price
        self.basePrice = basePrice
        self.number = number
        self.autoCPSFonts = {"titleFont": pygame.font.Font(r"C:\Windows\Fonts\REFSAN.TTF", 26),
                             "descFont": pygame.font.Font(r"C:\Windows\Fonts\REFSAN.TTF", 20),
                             "levelFont": pygame.font.Font(r"C:\Windows\Fonts\REFSAN.TTF", 24)}
        self.outline = pygame.Rect((25, (self.number - 1) * 100 + 20), (350, 100))
        self.descText = self.autoCPSFonts["descFont"].render(self.description, True, purple)
        self.imageRect = self.image.get_rect(center=(60, (60 + 100 * (self.number - 1))))
        self.descRect = self.descText.get_rect(center=(235, (self.number - 1) * 100 + 60))
        self.draw()

    def draw(self):
        self.titleText = self.autoCPSFonts["titleFont"].render(self.title + str(self.cps) + "CPS", True, purple)
        self.ownedText = self.autoCPSFonts["levelFont"].render("ИМЕЕТСЯ {}".format(self.owned), True, purple)
        self.buyText = self.autoCPSFonts["levelFont"].render("ЦЕНА {}".format(self.price), True, purple)
        self.CPSText = self.autoCPSFonts["levelFont"].render("МОЩНОСТЬ {}".format(self.cps), True, purple)
        self.ownedRect = self.ownedText.get_rect(center=(100, (self.number - 1) * 100 + 105))
        self.buyRect = self.titleText.get_rect(center=(300, (self.number - 1) * 100 + 105))
        self.powerRect = self.descText.get_rect(center=(220, (self.number - 1) * 100 + 40))

        if autoCPSMenuVisible:
            if self.number <= UNLOCKED_AUTOCPS:
                pygame.draw.rect(window, purple, self.outline, 5)
                window.blit(self.image, self.imageRect)
                window.blit(self.descText, self.descRect)
                window.blit(self.ownedText, self.ownedRect)
                window.blit(self.buyText, self.buyRect)

    def purchase(self):
        global COOKIES
        global CPS
        global UNLOCKED_AUTOCPS
        global UNLOCKED_UPGRADES
        COOKIES -= int(self.price)
        if self.owned == 3:
            UNLOCKED_AUTOCPS += 1
        if self.owned == 10:
            UNLOCKED_UPGRADES += 1


ChipCookie = Cookie(475, 300, 9, COOKIES)
grandMotherCPS = AutoCPS(grandMotherImage, "Бабушка - ", "Бабушка готовит печенье", GRANDMOTHERS_CPS,
                         GRANDMOTHERS, " Всего бабушек", GRANDMOTHERS_PRICE, 100, 1)
farmsCPS = AutoCPS(farmImage, "Ферма - ", "Новый вид земледелия", FARMS_CPS,
                         FARMS, " Всего ферм", FARMS_PRICE, 1000, 2)
minesCPS = AutoCPS(mineImage, "Шахта - ", "Майнинг печенья", MINES_CPS,
                         MINES, " Всего шахт", MINES_PRICE, 10000, 3)
factoryCPS = AutoCPS(factoryImage, "Фабрика - ", "Производит печенья", FACTORIES_CPS,
                         FACTORIES, " Всего фабрик", FACTORIES_PRICE, 100000, 4)
banksCPS = AutoCPS(bankImage, "Банк - ", "Stonks!!!", BANKS_CPS,
                         BANKS, " Всего банков", BANKS_PRICE, 1000000, 5)
cursorUpgrade = Upgrade(cursorUpgradeImage, "Апгрейд курсора", "Удвоение дохода от кликов", CURSOR_LEVEL, CURSOR_PRICE,
                        1, True)
grandMotherUpgrade = Upgrade(grandMotherUpgradeImage, "Апгрейд бабушек", "Удвоение дохода от бабушек",
                             GRANDMOTHERS_LEVEL, GRANDMOTHERS_UPGRADE_PRICE, 2)
farmUpgrade = Upgrade(farmUpgradeImage, "Апгрейд фермы", "Удвоение дохода от ферм", FARMS_LEVEL,
                      FARMS_UPGRADE_PRICE, 3)
mineUpgrade = Upgrade(mineUpgradeImage, "Апгрейд шахты", "Удвоение дохода от шахт", MINES_LEVEL,
                      MINES_UPGRADE_PRICE, 4)
factoryUpgrade = Upgrade(factoryUpgradeImage, "Апгрейд фабрики", "Удвоение дохода от фабрик", FACTORIES_LEVEL,
                         FACTORIES_UPGRADE_PRICE, 5)


def save():
    f = open("config.csv", mode="w")
    f.write("COOKIES,CPS,UNLOCKED_AUTOCPS,UNLOCKED_UPGRADES,GRANDMOTHERS,GRANDMOTHERS_PRICE,GRANDMOTHERS_CPS,FARMS,FARMS_PRICE,FARMS_CPS,MINES,MINES_PRICE,MINES_CPS,FACTORIES,FACTORIES_PRICE,FACTORIES_CPS,BANKS,BANKS_PRICE,BANKS_CPS,CURSOR_PRICE,CURSOR_LEVEL,CURSOR_POWER,GRANDMOTHERS_UPGRADE_PRICE,GRANDMOTHERS_LEVEL,FARMS_UPGRADE_PRICE,FARMS_LEVEL,MINES_UPGRADE_PRICE,MINES_LEVEL,FACTORIES_UPGRADE_PRICE,FACTORIES_LEVEL\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(ChipCookie.COOKIES, countCPS(), UNLOCKED_AUTOCPS, UNLOCKED_UPGRADES, grandMotherCPS.owned, grandMotherCPS.price, GRANDMOTHERS_CPS, farmsCPS.owned, farmsCPS.price, FARMS_CPS, minesCPS.owned, minesCPS.price, MINES_CPS, factoryCPS.owned, factoryCPS.price, FACTORIES_CPS, banksCPS.owned, banksCPS.price, BANKS_CPS, cursorUpgrade.price, cursorUpgrade.level, CURSOR_POWER, grandMotherUpgrade.price, grandMotherUpgrade.level, farmUpgrade.price, farmUpgrade.level, mineUpgrade.price, mineUpgrade.level, factoryUpgrade.price, factoryUpgrade.level))
    f.close()


def UpdateAll():
    ChipCookie.draw()
    drawMenuButtons()
    drawMenus()
    drawSaveButton()
    grandMotherCPS.draw()
    farmsCPS.draw()
    minesCPS.draw()
    factoryCPS.draw()
    banksCPS.draw()
    cursorUpgrade.draw()
    grandMotherUpgrade.draw()
    farmUpgrade.draw()
    mineUpgrade.draw()
    factoryUpgrade.draw()


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            print(x, y)

            if 96 <= x < 305 and 535 <= y < 592:
                if autoCPSMenuVisible:
                    autoCPSMenuVisible = False
                else:
                    autoCPSMenuVisible = True
                print(autoCPSMenuVisible)

            elif 656 <= x < 850 and 535 <= y < 592:
                if upgradeMenuVisible:
                    upgradeMenuVisible = False
                else:
                    upgradeMenuVisible = True

            elif (not autoCPSMenuVisible) and (not upgradeMenuVisible) and\
                    ChipCookie.rect.collidepoint(pygame.mouse.get_pos()):
                COOKIES += CURSOR_POWER
                ChipCookie.COOKIES = COOKIES

            if COOKIES >= grandMotherCPS.price and autoCPSMenuVisible and 26 <= x < 370 and 22 <= y < 117:
                COOKIES -= grandMotherCPS.price
                ChipCookie.COOKIES = COOKIES
                grandMotherCPS.owned += 1
                help[1] += 1
                grandMotherCPS.price = int((grandMotherCPS.price * 1.15) // 1) + 1
                UpdateAll()
                if grandMotherCPS.owned == 3:
                    UNLOCKED_AUTOCPS = 2
                if grandMotherCPS.owned == 10:
                    UNLOCKED_UPGRADES = 2

            if COOKIES >= farmsCPS.price and autoCPSMenuVisible and 26 <= x < 370 and 122 <= y < 217:
                COOKIES -= farmsCPS.price
                ChipCookie.COOKIES = COOKIES
                farmsCPS.owned += 1
                help[2] += 10
                farmsCPS.price = int((farmsCPS.price * 1.15) // 1) + 1
                UpdateAll()
                if farmsCPS.owned == 3:
                    UNLOCKED_AUTOCPS = 3
                if farmsCPS.owned == 10:
                    UNLOCKED_UPGRADES = 3

            if COOKIES >= minesCPS.price and autoCPSMenuVisible and 26 <= x < 370 and 222 <= y < 317:
                COOKIES -= minesCPS.price
                ChipCookie.COOKIES = COOKIES
                minesCPS.owned += 1
                help[3] += 100
                minesCPS.price = int((minesCPS.price * 1.15) // 1) + 1
                UpdateAll()
                if minesCPS.owned == 3:
                    UNLOCKED_AUTOCPS = 4
                if minesCPS.owned == 10:
                    UNLOCKED_UPGRADES = 4

            if COOKIES >= factoryCPS.price and autoCPSMenuVisible and 26 <= x < 370 and 322 <= y < 417:
                COOKIES -= factoryCPS.price
                ChipCookie.COOKIES = COOKIES
                factoryCPS.owned += 1
                help[4] += 1000
                factoryCPS.price = int((factoryCPS.price * 1.15) // 1) + 1
                UpdateAll()
                if factoryCPS.owned == 3:
                    UNLOCKED_AUTOCPS = 5
                if factoryCPS.owned == 10:
                    UNLOCKED_UPGRADES = 5

            if COOKIES >= banksCPS.price and autoCPSMenuVisible and 26 <= x < 370 and 422 <= y < 517:
                COOKIES -= banksCPS.price
                ChipCookie.COOKIES = COOKIES
                CPS += 10000
                banksCPS.owned += 1
                banksCPS.price = int((banksCPS.price * 1.15) // 1) + 1
                UpdateAll()
                save()

            if COOKIES >= cursorUpgrade.price and upgradeMenuVisible and 570 <= x < 922 and 22 <= y < 117:
                COOKIES -= cursorUpgrade.price
                ChipCookie.COOKIES = COOKIES
                CURSOR_POWER *= 2
                cursorUpgrade.price = int((cursorUpgrade.price * 1.15) // 1) + 1
                UpdateAll()
                save()

            if COOKIES >= grandMotherUpgrade.price and upgradeMenuVisible and 570 <= x < 922 and 122 <= y < 217:
                COOKIES -= grandMotherUpgrade.price
                ChipCookie.COOKIES = COOKIES
                grandMotherUpgrade.level += 1
                grandMotherUpgrade.price = int((grandMotherUpgrade.price * 1.15) // 1) + 1
                UpdateAll()
                save()

            if COOKIES >= farmUpgrade.price and upgradeMenuVisible and 570 <= x < 922 and 222 <= y < 317:
                COOKIES -= farmUpgrade.price
                ChipCookie.COOKIES = COOKIES
                farmUpgrade.level += 1
                farmUpgrade.price = int((farmUpgrade.price * 1.15) // 1) + 1
                UpdateAll()
                save()

            if COOKIES >= mineUpgrade.price and upgradeMenuVisible and 570 <= x < 922 and 322 <= y < 417:
                COOKIES -= mineUpgrade.price
                ChipCookie.COOKIES = COOKIES
                mineUpgrade.level += 1
                mineUpgrade.price = int((mineUpgrade.price * 1.15) // 1) + 1
                UpdateAll()
                save()

            if COOKIES >= factoryUpgrade.price and upgradeMenuVisible and 570 <= x < 922 and 422 <= y < 517:
                COOKIES -= factoryUpgrade.price
                ChipCookie.COOKIES = COOKIES
                factoryUpgrade.level += 1
                factoryUpgrade.price = int((factoryUpgrade.price * 1.15) // 1) + 1
                UpdateAll()
                save()

            if (not autoCPSMenuVisible) and (not upgradeMenuVisible) and 357 <= x < 613 and 537 <= y < 593:
                save()

    if 0 < ChipCookie.var <= 10:
        pygame.time.delay(100)
        ChipCookie.rect[1] += 1
        ChipCookie.var -= 1
        UpdateAll()
    elif 0 >= ChipCookie.var > -10:
        pygame.time.delay(100)
        ChipCookie.rect[1] -= 1
        ChipCookie.var -= 1
        UpdateAll()
    else:
        pygame.time.delay(100)
        ChipCookie.var = 10
        UpdateAll()

    timeCounter += clock.tick()
    if timeCounter >= 1000:
        COOKIES += countCPS()
        ChipCookie.COOKIES = COOKIES
        timeCounter = 0

    UpdateAll()
    pygame.display.flip()

pygame.quit()
exit()