(function () {
    'use strict';

    function pluriel(nombre) {
        return nombre > 1 ? 'places' : 'place';
    }

    function initialiserCompteurPlaces() {
        var formulaire = document.querySelector('[data-testid="booking-form"]');
        var champ = document.getElementById('places');
        var compteur = document.querySelector('[data-testid="places-counter"]');

        if (!formulaire || !champ || !compteur) {
            return;
        }

        var maximum = Number(formulaire.dataset.max || champ.max || 0);
        var solde = Number(formulaire.dataset.points || 0);

        function mettreAJour() {
            var valeur = Number(champ.value);
            compteur.classList.remove('booking-counter--warning');

            if (!champ.value || !Number.isFinite(valeur) || valeur < 1) {
                compteur.textContent = 'Saisissez un nombre de places.';
                return;
            }

            var detail = valeur + ' ' + pluriel(valeur) + ' = ' + valeur;
            detail += valeur > 1 ? ' points' : ' point';

            if (valeur > maximum) {
                compteur.textContent = detail + ' · maximum ' + maximum + ' places par achat.';
                compteur.classList.add('booking-counter--warning');
                return;
            }

            if (valeur > solde) {
                compteur.textContent = detail + ' · solde insuffisant : ' + solde + ' points disponibles.';
                compteur.classList.add('booking-counter--warning');
                return;
            }

            compteur.textContent = detail + ' · réservation possible.';
        }

        champ.addEventListener('input', mettreAJour);
        mettreAJour();
    }

    function trierTableauPoints() {
        var tableau = document.querySelector('[data-testid="points-table"]');
        if (!tableau || !tableau.tBodies.length) {
            return;
        }

        var corps = tableau.tBodies[0];
        var lignes = Array.prototype.slice.call(corps.rows);

        lignes.sort(function (a, b) {
            return Number(b.dataset.points || 0) - Number(a.dataset.points || 0);
        });

        lignes.forEach(function (ligne) {
            corps.appendChild(ligne);
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        initialiserCompteurPlaces();
        trierTableauPoints();
    });
}());
