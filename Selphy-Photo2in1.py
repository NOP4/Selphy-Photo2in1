#!/usr/bin/env python3

##########################################################
##                                                      ##
##          SCRIPT pour imprimante CANON SELPHY         ##
##                                                      ##
##    Ce script permet d'imprimer deux photos en une    ##
##       et d'obtenir une qualité sans comparaison      ##
##    avec la fonction correspondante de l'imprimante   ##
##                                                      ##
##                https://github.com/NOP4               ##
##                                                      ##
##########################################################
##                                                      ##
## Créer deux répertoires : IN ou OUT                   ##
## Placer les photos à concaténer dans le réperoite IN  ##
## La sortie est dans le répertoire OUT                 ##
##                                                      ##
## Certains paramètres sont personnalisables.           ##
## Voir les variables en début de script.               ##
##                                                      ##
## Limitation : à lancer sur des images de taille       ##
## similaire (peu importe l'orientation) car les        ##
## dimensions des images ne sont pas redimentionnées    ##
## pour limiter les écarts de dimension.                ##
##                                                      ##
##########################################################

## Nécessite Pillow : pip3 install Pillow

import sys
from PIL import Image
from os import listdir
from os.path import isfile, join

couleur_fond = "#FFFFFF"
ratio_attendu = 15/10
path_in = "IN"
path_out = "OUT"
separateur_images = 50
marge = 5 #en mm
largeur_impression = 150 #en mm
hauteur_impression = 100 #en mm


def concateneImage2in1(nom_sortie, nom_image1, nom_image2):
    global separateur_images, couleur_fond, ratio_attendu

    image1 = Image.open(nom_image1)
    image2 = Image.open(nom_image2)

    print("Image 1")
    print("   x = " + str(image1.width))
    print("   y = " + str(image1.height))
    # Rotation de l'image si besoin
    if image1.width > image1.height:
      print("   Rotation de l'image")
      image1 = image1.rotate(90, 0, 1)
      print("   x = " + str(image1.width))
      print("   y = " + str(image1.height))

    print("Image 2")
    print("   x = " + str(image2.width))
    print("   y = " + str(image2.height))
    # Rotation de l'image si besoin
    if image2.width > image2.height:
      print("   Rotation de l'image")
      image2 = image2.rotate(90, 0, 1)
      print("   x = " + str(image2.width))
      print("   y = " + str(image2.height))

    tmp_img_width = image1.width + separateur_images + image2.width
    tmp_img_height = max(image1.height, image2.height)

    print("Image concaténée initiale")
    print("   x = " + str(tmp_img_width))
    print("   y = " + str(tmp_img_height))
    print("   ratio = " + str(tmp_img_width/tmp_img_height))

    # Calcul du ratio de l'image. Passage en ratio 2/3 si besoin
    # Calcul de la taille de l'image finale
    ratio_initial = tmp_img_width / tmp_img_height
    print("Ratio initial = " + str(ratio_initial))
    print("Ratio attendu = " + str(ratio_attendu))
    final_decal_x = 0
    final_decal_y = 0
    final_width = tmp_img_width
    final_height = tmp_img_height
    if ratio_attendu > ratio_initial:
        print("On étire l'image en largeur")
        # final_width / final_height =  ratio_attendu
        # (tmp_img_width * ratio) / tmp_img_height = ratio_attendu
        # => ratio = (ratio_attendu * tmp_img_height) / tmp_img_width
        # ==> final_width = tmp_img_width * ratio
        # ===> final_width = tmp_img_width * (ratio_attendu * tmp_img_height) / tmp_img_width
        final_width = int( tmp_img_width * (ratio_attendu * tmp_img_height) / tmp_img_width )
        final_decal_x = int( (final_width - tmp_img_width) / 2 )
        print("Nouvelle largeur = " + str(final_width))
    else:
        if ratio_attendu < ratio_initial:
            print("On étire l'image en hauteur")
            final_height = int( tmp_img_height * (tmp_img_width / ratio_attendu) / tmp_img_height )
            final_decal_y = int( (final_height - tmp_img_height) / 2 )
            # idem précédemment en intervertissant width et height
        else:
            # le ratio est déjà bon, on garde les valeurs de decal_x et decal_y à 0
            # et final_height et final_width sont à conserver
            pass

    new_im = Image.new('RGB', (final_width, final_height), couleur_fond)
    new_im.paste(image1, (final_decal_x, final_decal_y))
    new_im.paste(image2, (final_decal_x+image1.width+separateur_images, final_decal_y))

    print("Image finale")
    print("   x = " + str(new_im.width))
    print("   y = " + str(new_im.height))
    print("   ratio = " + str(new_im.width/new_im.height))

    # ajout des marges
    final2_width = int((final_width/largeur_impression)*marge)+final_width
    final2_height = int((final_height/hauteur_impression)*marge)+final_height
    new_im2 = Image.new('RGB', (final2_width, final2_height), couleur_fond)
    new_im2.paste(new_im, (int((final2_width-final_width)/2), int((final2_height-final_height)/2)))

    # sauvegarde du fichier
    new_im2.save(nom_sortie)


files = [
        f for f in listdir(path_in)
        if (
            isfile(join(path_in, f))
            and
            (f.endswith('.JPG') or f.endswith('.jpg'))
        )
    ]
files.sort()

etape = 1
filename1 = ""
filename2 = ""
out_cpt = 1
for f in files:
    if etape == 1:
        filename1 = f
        etape = 2
    else:
        #etape = 2
        filename2 = f
        etape = 1
        concateneImage2in1(path_out + '/' + str(out_cpt).zfill(4) + '.jpg', path_in + '/' + filename1, path_in + '/' + filename2)
        out_cpt+=1

if etape == 2:
    #on n'a qu'une image sur la dernière photo, on l'imprime 2 fois
    filename2 = filename1
    concateneImage2in1(path_out + '/' + str(out_cpt).zfill(4) + '.jpg', path_in + '/' + filename1, path_in + '/' + filename2)
    out_cpt+=1
