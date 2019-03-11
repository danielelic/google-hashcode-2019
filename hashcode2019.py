#
# Google Hash Code 2019
#
# Copyright (c) 2019 Team "DeepDev Team"
#
# Version 1.0
# Daniele Liciotti
# Laura Montanini
#
import sys
import os


def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]


def interestFactor(s1, s2):
    a = len(intersection(s1, s2))
    b = len(intersection(s2, s1))
    c = len(list(set(s1 + s2)))
    return min([a, b, c]), max([a, b, c])


class Slide:
    def __init__(self, idx, pics, tags):
        self.idx = idx
        self.pics = pics
        self.tags = tags


class Photo:
    def __init__(self, idx, direction, tags):
        self.idx = idx
        self.direction = direction
        self.tags = tags


def read_file(filename):
    with open(filename, 'r') as f:
        line = f.readline()
        no_photos = int(line.split()[0])
        photosH = []
        photosV = []
        for idx in range(no_photos):
            if not (idx % 500):
                print("Loading:\t" + str(idx) + "/" + str(no_photos))
            photo_info = f.readline().split()
            direction = photo_info[0]

            tags = photo_info[-int(photo_info[1]):]
            if direction == 'H':
                photosH.append(Photo(idx=idx, direction=direction, tags=tags))
            if direction == 'V':
                photosV.append(Photo(idx=idx, direction=direction, tags=tags))
    photosV.sort(key=lambda s: len(s.tags), reverse=True)
    photosH.sort(key=lambda s: len(s.tags), reverse=True)
    print("Pics H:\t" + str(len(photosH)))
    print("Pics V:\t" + str(len(photosV)))
    return photosH, photosV



def write_file(sequence, filename):
    '''
    Write the output file
    '''
    with open(filename, 'w') as f:
        f.write('{}\n'.format(len(sequence)))
        for el in sequence:
            f.write(' '.join([str(item) for item in el[1]]) + '\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Syntax: %s <filename>' % sys.argv[0])

    print('Running on file ', sys.argv[1])

    filename = sys.argv[1]
    photosListH, photosListV = read_file(filename)
    slidesH = [Slide(i, [el.idx], el.tags) for i, el in enumerate(photosListH)]
    slidesV = []
    sequence = []

    if (len(slidesH)):
        sequence.append((slidesH[0].idx, slidesH[0].pics))
        latestSlide = slidesH[0]
        slidesH.pop(0)

    else:
        slidesV.append(
            Slide(0, [photosListV[0].idx, photosListV[1].idx],
                  list(set(photosListV[0].tags + photosListV[1].tags))))
        sequence.append((slidesV[0].idx, slidesV[0].pics))
        photosListV.pop(1)
        photosListV.pop(0)
        latestSlide = slidesV[0]
        slidesV.pop(0)

    print("Slides H:\t" + str(len(slidesH)))
    print("Slides V:\t" + str(len(slidesV)))

    listV = []
    for k, photok in enumerate(photosListV):
        check_union = False
        min_inter = 0
        if photok.idx not in listV:
            while not (check_union):
                for y, photoy in enumerate(photosListV):
                    if (y > k and photoy.idx not in listV) or y == len(photosListV) - 1:
                        lenTags = len(intersection(photok.tags, photoy.tags))
                        if (lenTags == min_inter) or y == len(photosListV) - 1:
                            try:
                                idx = (slidesV[-1].idx) + 1
                            except IndexError:
                                idx = 0
                            slidesV.append(Slide(idx,
                                                 [photok.idx, photoy.idx],
                                                 list(set(photok.tags + photoy.tags))))
                            print(len(slidesV), len(slidesV[-1].tags), [photok.idx, photoy.idx])
                            listV.append(photok.idx)
                            listV.append(photoy.idx)
                            check_union = True
                            break
                min_inter += 1
    del listV
    slidesV.sort(key=lambda s: len(s.tags))
    print("Slides V:\t" + str(len(slidesV)))

    matrix = []
    iFactorsV = []
    iFactorsH = []

    while len(slidesH + slidesV):
        iFacH = None
        iGapH = None
        iFacV = None
        iGapV = None
        skipV = False

        for i, e in enumerate(slidesH):
            if e != latestSlide:
                iFac, iGap = interestFactor(latestSlide.tags, e.tags)
                if iFacH == None or iFac > iFacH:
                    iFacH = iFac
                    iGapH = iGap
                    idxH = i
                elif iFac == iFacH and iGap < iGapH:
                    iGapH = iGap
                    idxH = i
            if iFacH == int(len(latestSlide.tags) / 2) and int(len(e.tags) / 2):
                skipV = True
                break
        if not skipV:
            for i, e in enumerate(slidesV):
                if e != latestSlide:
                    iFac, iGap = interestFactor(latestSlide.tags, e.tags)
                    if iFacV == None or iFac > iFacV:
                        iFacV = iFac
                        iGapV = iGap
                        idxV = i
                    elif iFac == iFacV and iGap < iGapV:
                        iGapV = iGap
                        idxV = i
                if iFacV == int(len(latestSlide.tags) / 2) and int(len(e.tags) / 2):
                    break

        if sequence == []:
            if len(slidesV) > 0:
                sequence.append((slidesV[0].idx, slidesV[0].pics))
            elif len(slidesH) > 0:
                sequence.append((slidesH[0].idx, slidesH[0].pics))
            break
        if iFacV != None and iFacH != None and iFacV == iFacH:
            if iGapV < iGapH:
                sequence.append((slidesV[idxV].idx, slidesV[idxV].pics))
                latestSlide = slidesV[idxV]
                slidesV.pop(idxV)
            else:
                sequence.append((slidesH[idxH].idx, slidesH[idxH].pics))
                latestSlide = slidesH[idxH]
                slidesH.pop(idxH)
        elif iFacV != None and iFacH != None and iFacV > iFacH:
            sequence.append((slidesV[idxV].idx, slidesV[idxV].pics))
            latestSlide = slidesV[idxV]
            slidesV.pop(idxV)
        elif iFacV == None and iFacH != None:
            sequence.append((slidesH[idxH].idx, slidesH[idxH].pics))
            latestSlide = slidesH[idxH]
            slidesH.pop(idxH)
        elif iFacH == None and iFacV != None:
            sequence.append((slidesV[idxV].idx, slidesV[idxV].pics))
            latestSlide = slidesV[idxV]
            slidesV.pop(idxV)
        else:
            sequence.append((slidesH[idxH].idx, slidesH[idxH].pics))
            latestSlide = slidesH[idxH]
            slidesH.pop(idxH)

        print("V =", len(slidesV),
              "\tH =", len(slidesH),
              "\tSeq_size =", len(sequence),
              "\tPhoto(s) =", sequence[-1][-1])

    write_file(sequence, filename + '.out')
    os.system('zip hashcode2019.zip -r hashcode2019.py')
