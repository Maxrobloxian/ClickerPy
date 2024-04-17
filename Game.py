import random

class Weapon:

    __actual_ammo = int

    def __weapon(self, speed, magazine, bps):
        self.__speed = speed
        self.__magazine_size = magazine
        self.__bullets_per_shot = bps
        self.__actual_ammo = magazine

    def choseWeapon(self, weapon = int):
        if (weapon == 1):
            self.__weapon(self, 6, 15, 1)
        elif (weapon == 2):
            self.__weapon(self, 14, 30, 1)
        elif (weapon == 3):
            self.__weapon(self, 4, 5, 3)
        else:
            w = int(input("No weapon found, try again: 1.Pistol 2.M4 3.Shotgun"))
            self.choseWeapon(self, w)

    def change_actual_ammo(self):
        self.__actual_ammo -= 1

    def reload(self):
        self.__actual_ammo = self.__magazine_size

    def get_weapon_details(self, option = int):
        if (option == 1):
            return self.__speed
        elif (option == 2):
            return self.__magazine_size
        elif (option == 3):
            return self.__bullets_per_shot
        
    def get_actual_ammo(self):
        return self.__actual_ammo

class Targets:

    __num_of_enemies = int

    def set_targets(self, enemies = int, citizens = int, enem_skill = int):
        self.__num_of_enemies = enemies
        self.__num_of_citizens = citizens
        self.__enemies_skill = enem_skill

    def decrease_enemies(self, ammount = int):
        self.__num_of_enemies -= ammount

    def decrease_citizens(self, ammount = int):
        self.__num_of_citizens -= ammount

    def get_targets(self, option = int):
        if (option == 1):
            return self.__num_of_enemies
        elif (option == 2):
            return self.__num_of_citizens
        elif (option == 3):
            return self.__enemies_skill
        else:
            return self.__num_of_enemies, self.__num_of_citizens, self.__enemies_skill
    
class Player:

    __skill = 20
    game_difficulty = int
    prev_dif = int
    __inc_skill = True
    __life = 100

    def set_player_life(self, ammount = int):
        self.__life = ammount

    def set_skill(self, ammount = int):
        if (self.prev_dif != self.game_difficulty):
            self.__skill = ammount
            self.__inc_skill = False

    def icrease_skill(self, ammount = int):
        if (self.__skill < 100 and self.__inc_skill):
            self.__skill += ammount
            if (self.__skill > 100):
                self.__skill = 100
        else:
            self.__inc_skill = True

    def change_player_life(self, ammount):
        self.__life += ammount
    
    def get_player_skill(self):
        return self.__skill
    
    def get_player_life(self):
        return self.__life
    
    def player_ded(self):
        print("You died lol")

class Game:

    __play_nr = 0
    __round_nr = 0

    def play(self):
        Player.set_player_life(Player, 100)
        self.__set_difficulty(int(input("Choose difficulty: 1.Easy 2.Normal 3.Hard 4.Custom ")))

        self.__decide_skill_level()

        print("Player life:",Player.get_player_life(Player), "skill:", Player.get_player_skill(Player))
        print("Number of enemies:", Targets.get_targets(Targets,1), "citizens:", Targets.get_targets(Targets,2))

        Weapon.choseWeapon(Weapon, int(input("Choose a weapon: 1.Pistol 2.M4 3.Shotgun ")))

        while (Player.get_player_life(Player) > 0 and Targets.get_targets(Targets, 1) > 0):
            self.__kill_suff()
            self.__round_nr += 1
            if (self.__round_nr == 5):
                self.__take_damage()
                self.__round_nr = 0

        self.__win_lose_state()

        # Keep at bottom !!!!!!
        self.__restart()

    def __decide_skill_level(self):
        if (self.__play_nr == 0):
            self.__play_nr += 1
            Player.icrease_skill(Player, 0)
        else:
            Player.icrease_skill(Player, 20)

    def __set_difficulty(self, difficulty):
        Player.game_difficulty = difficulty

        if (difficulty == 1):
            Targets.set_targets(Targets, 50, 0, 20)
            Player.set_skill(Player, 100)
        elif (difficulty == 2):
            Targets.set_targets(Targets, 80, 20, 50)
            Player.set_skill(Player, 50)
        elif (difficulty == 3):
            Targets.set_targets(Targets, 110, 50, 80)
            Player.set_skill(Player, 20)
        elif (difficulty == 4):
            Targets.set_targets(Targets, int(input("")), int(input("")), int(input("")))
            Player.set_skill(Player, int(input("")))
        else:
            d = int(input("No difficulty found, try again: 1.Easy 2.Normal 3.Hard 4.Custom "))
            self.__set_difficulty(d)

        Player.prev_dif = difficulty

    def __kill_suff(self):
        self.__shoot()

    def __shoot(self):
        self.__chance_enem = Player.get_player_skill(Player)
        if (self.__chance_enem != 100):
            self.__chance_citiz = (100 - self.__chance_enem) / 2.5 + self.__chance_enem
        else:
            self.__chance_citiz = -1

        self.__enemies_killed, self.__citizens_killed, self.__missed = 0, 0, 0
        self.__no_Ammo = False
        for i in range(Weapon.get_weapon_details(Weapon, 1)):
            Weapon.change_actual_ammo(Weapon)
            self.__lucky_guess = random.randint(0,100)
            if (self.__lucky_guess <= self.__chance_enem and Targets.get_targets(Targets, 1) and Weapon.get_actual_ammo(Weapon) > 0):
                Targets.decrease_enemies(Targets, 1)
                self.__enemies_killed += 1
            elif (self.__lucky_guess > self.__chance_enem and self.__lucky_guess <= self.__chance_citiz and Targets.get_targets(Targets, 2) and Weapon.get_actual_ammo(Weapon) > 0):
                Targets.decrease_citizens(Targets, 1)
                self.__citizens_killed += 1
            elif (Weapon.get_actual_ammo(Weapon) <= 0):
                Weapon.reload(Weapon)
                print("You killed:", self.__enemies_killed,"Enemies,", self.__citizens_killed, "Citizens and missed", self.__missed, "shots, ran out of ammo and had to hide")
                self.__no_Ammo = True
                break
            else:
                self.__missed += 1
        
        if (self.__no_Ammo == False):
            print("You killed:", self.__enemies_killed,"Enemies,", self.__citizens_killed, "Citizens and missed", self.__missed, "shots")

    def __take_damage(self):
        self.__took_damage = False
        self.__damage_taken = 0
        for n in range(Targets.get_targets(Targets, 1)):
            self.__lucky_guess = random.randint(0,100)
            if (Player.get_player_life(Player) == 0):
                Player.player_ded(Player)
                break
            elif (self.__lucky_guess <= Targets.get_targets(Targets, 3)):
                Player.change_player_life(Player,-1)
                self.__took_damage = True
                self.__damage_taken += 1
       
        if (self.__took_damage):
            print("The enemies shot you, and lost", self.__damage_taken, "Health")

    def __restart(self):
        self.G = input("Whant to play again? Press 'Enter' to restart, type anything no quit ")
        if (self.G == "" or self.G == "yes" or self.G == "Yes"):
            print("-------------------------------------------------------------------------")
            self.play()

    def __win_lose_state(self):
        if (Targets.get_targets(Targets, 1) <= 0 and Targets.get_targets(Targets, 2) >= 1):
            print("Congratulations, you won and saved", Targets.get_targets(Targets, 2), "citizens!")
        elif (Targets.get_targets(Targets, 1) <= 0 and Targets.get_targets(Targets, 2) <= 0):
            print("Congratulations, you won... but killed all the citizens")
            print("DEATH SENTENCE!!!!")

my_game = Game()

my_game.play()
# shotgun + colors