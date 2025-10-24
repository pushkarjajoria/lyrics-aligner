#!/bin/bash

set -euo pipefail

echo "Found 24 arias to process."

echo "[1/24] Running Bellini_Puritani_Suoni_la_tromba ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Bellini_Puritani_Suoni_la_tromba/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Bellini_Puritani_Suoni_la_tromba/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Bellini_Puritani_Suoni_la_tromba/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Bellini_Puritani_Suoni_la_tromba/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Bellini_Puritani_Suoni_la_tromba/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Bellini_Puritani_Suoni_la_tromba/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Bellini_Puritani_Suoni_la_tromba/separated_vocals/Bellini_Puritani_Suoni_la_tromba_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Bellini_Puritani_Suoni_la_tromba/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Bellini_Puritani_Suoni_la_tromba/separated_vocals/Bellini_Puritani_Suoni_la_tromba_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Bellini_Puritani_Suoni_la_tromba/spleeter_tmp"
echo "   → Done."

echo "[2/24] Running Handel_GiulioCesare_DaTempeste ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_DaTempeste/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_DaTempeste/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_DaTempeste/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_DaTempeste/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_DaTempeste/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_DaTempeste/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_DaTempeste/separated_vocals/Handel_GiulioCesare_DaTempeste_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_DaTempeste/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_DaTempeste/separated_vocals/Handel_GiulioCesare_DaTempeste_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_DaTempeste/spleeter_tmp"
echo "   → Done."

echo "[3/24] Running Handel_GiulioCesare_Empio ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Empio/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Empio/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Empio/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Empio/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Empio/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Empio/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Empio/separated_vocals/Handel_GiulioCesare_Empio_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Empio/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Empio/separated_vocals/Handel_GiulioCesare_Empio_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Empio/spleeter_tmp"
echo "   → Done."

echo "[4/24] Running Handel_GiulioCesare_Piangero ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Piangero/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Piangero/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Piangero/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Piangero/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Piangero/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Piangero/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Piangero/separated_vocals/Handel_GiulioCesare_Piangero_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Piangero/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Piangero/separated_vocals/Handel_GiulioCesare_Piangero_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Piangero/spleeter_tmp"
echo "   → Done."

echo "[5/24] Running Handel_GiulioCesare_Se_in_Fiorito ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Se_in_Fiorito/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Se_in_Fiorito/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Se_in_Fiorito/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Se_in_Fiorito/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Se_in_Fiorito/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Se_in_Fiorito/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Se_in_Fiorito/separated_vocals/Handel_GiulioCesare_Se_in_Fiorito_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Se_in_Fiorito/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Se_in_Fiorito/separated_vocals/Handel_GiulioCesare_Se_in_Fiorito_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Se_in_Fiorito/spleeter_tmp"
echo "   → Done."

echo "[6/24] Running Handel_GiulioCesare_VaTacito ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_VaTacito/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_VaTacito/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_VaTacito/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_VaTacito/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_VaTacito/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_VaTacito/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_VaTacito/separated_vocals/Handel_GiulioCesare_VaTacito_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_VaTacito/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_VaTacito/separated_vocals/Handel_GiulioCesare_VaTacito_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_VaTacito/spleeter_tmp"
echo "   → Done."

echo "[7/24] Running Handel_GiulioCesare_Vadoro_Pupille ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Vadoro_Pupille/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Vadoro_Pupille/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Vadoro_Pupille/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Vadoro_Pupille/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Vadoro_Pupille/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Vadoro_Pupille/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Vadoro_Pupille/separated_vocals/Handel_GiulioCesare_Vadoro_Pupille_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Vadoro_Pupille/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Vadoro_Pupille/separated_vocals/Handel_GiulioCesare_Vadoro_Pupille_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Handel_GiulioCesare_Vadoro_Pupille/spleeter_tmp"
echo "   → Done."

echo "[8/24] Running Mozart_DonGiovanni_Madamina ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_DonGiovanni_Madamina/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_DonGiovanni_Madamina/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_DonGiovanni_Madamina/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_DonGiovanni_Madamina/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_DonGiovanni_Madamina/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_DonGiovanni_Madamina/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_DonGiovanni_Madamina/separated_vocals/Mozart_DonGiovanni_Madamina_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_DonGiovanni_Madamina/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_DonGiovanni_Madamina/separated_vocals/Mozart_DonGiovanni_Madamina_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_DonGiovanni_Madamina/spleeter_tmp"
echo "   → Done."

echo "[9/24] Running Mozart_Nozze_Deh_vieni ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Deh_vieni/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Deh_vieni/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Deh_vieni/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Deh_vieni/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Deh_vieni/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Deh_vieni/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Deh_vieni/separated_vocals/Mozart_Nozze_Deh_vieni_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Deh_vieni/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Deh_vieni/separated_vocals/Mozart_Nozze_Deh_vieni_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Deh_vieni/spleeter_tmp"
echo "   → Done."

echo "[10/24] Running Mozart_Nozze_Non_so_più ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Non_so_più/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Non_so_più/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Non_so_più/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Non_so_più/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Non_so_più/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Non_so_più/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Non_so_più/separated_vocals/Mozart_Nozze_Non_so_più_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Non_so_più/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Non_so_più/separated_vocals/Mozart_Nozze_Non_so_più_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Non_so_più/spleeter_tmp"
echo "   → Done."

echo "[11/24] Running Mozart_Nozze_Se_vuol_ballare ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Se_vuol_ballare/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Se_vuol_ballare/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Se_vuol_ballare/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Se_vuol_ballare/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Se_vuol_ballare/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Se_vuol_ballare/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Se_vuol_ballare/separated_vocals/Mozart_Nozze_Se_vuol_ballare_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Se_vuol_ballare/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Se_vuol_ballare/separated_vocals/Mozart_Nozze_Se_vuol_ballare_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Mozart_Nozze_Se_vuol_ballare/spleeter_tmp"
echo "   → Done."

echo "[12/24] Running Norma_Casta Diva ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Norma_Casta Diva/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Norma_Casta Diva/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Norma_Casta Diva/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Norma_Casta Diva/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Norma_Casta Diva/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Norma_Casta Diva/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Norma_Casta Diva/separated_vocals/Norma_Casta Diva_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Norma_Casta Diva/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Norma_Casta Diva/separated_vocals/Norma_Casta Diva_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Norma_Casta Diva/spleeter_tmp"
echo "   → Done."

echo "[13/24] Running Puccini_Turandot_Nessun_dorma ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Puccini_Turandot_Nessun_dorma/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Puccini_Turandot_Nessun_dorma/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Puccini_Turandot_Nessun_dorma/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Puccini_Turandot_Nessun_dorma/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Puccini_Turandot_Nessun_dorma/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Puccini_Turandot_Nessun_dorma/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Puccini_Turandot_Nessun_dorma/separated_vocals/Puccini_Turandot_Nessun_dorma_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Puccini_Turandot_Nessun_dorma/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Puccini_Turandot_Nessun_dorma/separated_vocals/Puccini_Turandot_Nessun_dorma_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Puccini_Turandot_Nessun_dorma/spleeter_tmp"
echo "   → Done."

echo "[14/24] Running Rigoletto_Pari siamo ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Pari siamo/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Pari siamo/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Pari siamo/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Pari siamo/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Pari siamo/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Pari siamo/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Pari siamo/separated_vocals/Rigoletto_Pari siamo_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Pari siamo/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Pari siamo/separated_vocals/Rigoletto_Pari siamo_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Pari siamo/spleeter_tmp"
echo "   → Done."

echo "[15/24] Running Rigoletto_Quel vecchio ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Quel vecchio/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Quel vecchio/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Quel vecchio/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Quel vecchio/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Quel vecchio/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Quel vecchio/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Quel vecchio/separated_vocals/Rigoletto_Quel vecchio_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Quel vecchio/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Quel vecchio/separated_vocals/Rigoletto_Quel vecchio_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rigoletto_Quel vecchio/spleeter_tmp"
echo "   → Done."

echo "[16/24] Running Rossini_Barbiere_A_un_dottor ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_A_un_dottor/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_A_un_dottor/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_A_un_dottor/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_A_un_dottor/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_A_un_dottor/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_A_un_dottor/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_A_un_dottor/separated_vocals/Rossini_Barbiere_A_un_dottor_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_A_un_dottor/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_A_un_dottor/separated_vocals/Rossini_Barbiere_A_un_dottor_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_A_un_dottor/spleeter_tmp"
echo "   → Done."

echo "[17/24] Running Rossini_Barbiere_Largo_al_factotum ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_Largo_al_factotum/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_Largo_al_factotum/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_Largo_al_factotum/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_Largo_al_factotum/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_Largo_al_factotum/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_Largo_al_factotum/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_Largo_al_factotum/separated_vocals/Rossini_Barbiere_Largo_al_factotum_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_Largo_al_factotum/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_Largo_al_factotum/separated_vocals/Rossini_Barbiere_Largo_al_factotum_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini_Barbiere_Largo_al_factotum/spleeter_tmp"
echo "   → Done."

echo "[18/24] Running Rossini__Barbiere_La_calunnia ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini__Barbiere_La_calunnia/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini__Barbiere_La_calunnia/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini__Barbiere_La_calunnia/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini__Barbiere_La_calunnia/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini__Barbiere_La_calunnia/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini__Barbiere_La_calunnia/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini__Barbiere_La_calunnia/separated_vocals/Rossini__Barbiere_La_calunnia_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini__Barbiere_La_calunnia/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini__Barbiere_La_calunnia/separated_vocals/Rossini__Barbiere_La_calunnia_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Rossini__Barbiere_La_calunnia/spleeter_tmp"
echo "   → Done."

echo "[19/24] Running Traviata_Sempre libera ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Traviata_Sempre libera/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Traviata_Sempre libera/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Traviata_Sempre libera/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Traviata_Sempre libera/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Traviata_Sempre libera/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Traviata_Sempre libera/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Traviata_Sempre libera/separated_vocals/Traviata_Sempre libera_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Traviata_Sempre libera/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Traviata_Sempre libera/separated_vocals/Traviata_Sempre libera_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Traviata_Sempre libera/spleeter_tmp"
echo "   → Done."

echo "[20/24] Running Trovatore_Di quella pira ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Trovatore_Di quella pira/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Trovatore_Di quella pira/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Trovatore_Di quella pira/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Trovatore_Di quella pira/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Trovatore_Di quella pira/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Trovatore_Di quella pira/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Trovatore_Di quella pira/separated_vocals/Trovatore_Di quella pira_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Trovatore_Di quella pira/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Trovatore_Di quella pira/separated_vocals/Trovatore_Di quella pira_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Trovatore_Di quella pira/spleeter_tmp"
echo "   → Done."

echo "[21/24] Running Verdi_Rigoletto_Caro_Nome ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Caro_Nome/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Caro_Nome/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Caro_Nome/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Caro_Nome/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Caro_Nome/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Caro_Nome/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Caro_Nome/separated_vocals/Verdi_Rigoletto_Caro_Nome_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Caro_Nome/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Caro_Nome/separated_vocals/Verdi_Rigoletto_Caro_Nome_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Caro_Nome/spleeter_tmp"
echo "   → Done."

echo "[22/24] Running Verdi_Rigoletto_Questa_o_Quella ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Questa_o_Quella/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Questa_o_Quella/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Questa_o_Quella/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Questa_o_Quella/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Questa_o_Quella/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Questa_o_Quella/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Questa_o_Quella/separated_vocals/Verdi_Rigoletto_Questa_o_Quella_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Questa_o_Quella/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Questa_o_Quella/separated_vocals/Verdi_Rigoletto_Questa_o_Quella_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Rigoletto_Questa_o_Quella/spleeter_tmp"
echo "   → Done."

echo "[23/24] Running Verdi_Traviata_De_miei_bollenti ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_De_miei_bollenti/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_De_miei_bollenti/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_De_miei_bollenti/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_De_miei_bollenti/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_De_miei_bollenti/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_De_miei_bollenti/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_De_miei_bollenti/separated_vocals/Verdi_Traviata_De_miei_bollenti_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_De_miei_bollenti/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_De_miei_bollenti/separated_vocals/Verdi_Traviata_De_miei_bollenti_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_De_miei_bollenti/spleeter_tmp"
echo "   → Done."

echo "[24/24] Running Verdi_Traviata_Di_Provenza ..."
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_Di_Provenza/separated_vocals"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_Di_Provenza/spleeter_tmp" || true
mkdir -p "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_Di_Provenza/spleeter_tmp"
spleeter separate -p spleeter:2stems -o "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_Di_Provenza/spleeter_tmp" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_Di_Provenza/audio/song.mp3"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_Di_Provenza/spleeter_tmp/song/vocals.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_Di_Provenza/separated_vocals/Verdi_Traviata_Di_Provenza_vocals.wav"
mv "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_Di_Provenza/spleeter_tmp/song/accompaniment.wav" "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_Di_Provenza/separated_vocals/Verdi_Traviata_Di_Provenza_accompaniment.wav"
rm -rf "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset/Verdi_Traviata_Di_Provenza/spleeter_tmp"
echo "   → Done."

echo "✅ All 24 separations completed."
