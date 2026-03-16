from .models import *
import random
import json
import math


class game(Page):
    form_model = 'player'
    form_fields = ['prospek_terpilih', 'kontribusi_persen']

    def error_message(self, values):
        if not values.get('prospek_terpilih'):
            return "Silakan pilih salah satu prospek investasi."
        if values.get('kontribusi_persen') is None:
            return "Silakan masukkan persentase kontribusi (0-100)."

    def vars_for_template(self):
        rd = Constants.rounds_data[self.round_number - 1]
        is_ambiguity = rd['round_type'] == 'ambiguity'
        treatment = self.session.config.get('treatment', 'by_return')

        # Untuk ronde risk, tampilkan prob pasti
        # Untuk ronde ambiguity, tampilkan "minimal X%"
        if is_ambiguity:
            # Display probabilities as "minimal X%"
            display_prob_a1 = f"minimal {int(rd['prob_a1'] * 100)}%"
            display_prob_a2 = f"sisanya"
            display_prob_b1 = f"minimal {int(rd['prob_b1'] * 100)}%"
            display_prob_b2 = f"sisanya"
            display_prob_damage = f"maksimal {int(rd['prob_damage'] * 100)}%"
        else:
            display_prob_a1 = f"{int(rd['prob_a1'] * 100)}%"
            display_prob_a2 = f"{int(rd['prob_a2'] * 100)}%"
            display_prob_b1 = f"{int(rd['prob_b1'] * 100)}%"
            display_prob_b2 = f"{int(rd['prob_b2'] * 100)}%"
            display_prob_damage = f"{int(rd['prob_damage'] * 100)}%"

        # Return sebagai multiplier display (format desimal Indonesia: 2,8x)
        def fmt_mult(v):
            if v == int(v):
                return str(int(v))
            return str(v).replace('.', ',')

        ret_a1_display = fmt_mult(rd['ret_a1'])
        ret_a2_display = f"{int(rd['ret_a2'] * 100)}%"
        ret_b1_display = fmt_mult(rd['ret_b1'])
        ret_b2_display = f"{int(rd['ret_b2'] * 100)}%"

        # Chart data (hanya untuk risk rounds)
        if not is_ambiguity:
            a_chart = dict(
                labels=[
                    f"{ret_a1_display}x lipat (prob {display_prob_a1})",
                    f"{ret_a2_display} (prob {display_prob_a2})",
                ],
                data=[int(rd['prob_a1'] * 100), int(rd['prob_a2'] * 100)],
            )
            b_chart = dict(
                labels=[
                    f"{ret_b1_display}x lipat (prob {display_prob_b1})",
                    f"{ret_b2_display} (prob {display_prob_b2})",
                ],
                data=[int(rd['prob_b1'] * 100), int(rd['prob_b2'] * 100)],
            )
        else:
            a_chart = None
            b_chart = None

        # Damage value
        damage_value = rd['damage_multiplier'] * rd['investasi']

        # Kontribusi text berdasarkan treatment
        if treatment == 'by_return':
            kontribusi_text = "dari nilai return yang diperoleh jika tidak terjadi kerusakan lingkungan"
        else:
            kontribusi_text = "dari nilai kapitalisasi perusahaan Anda, terlepas dari ada atau tidaknya kerusakan lingkungan"

        # Minimum prob pct for ambiguity bar visualization
        min_prob_a1_pct = int(rd['prob_a1'] * 100)
        min_prob_b1_pct = int(rd['prob_b1'] * 100)

        return dict(
            round_type=rd['round_type'],
            range_type=rd['range_type'],
            capital=rd['capital'],
            investasi=rd['investasi'],
            cc_inv=rd['cc_inv'],
            ret_a1=ret_a1_display,
            ret_a2=ret_a2_display,
            ret_b1=ret_b1_display,
            ret_b2=ret_b2_display,
            display_prob_a1=display_prob_a1,
            display_prob_a2=display_prob_a2,
            display_prob_b1=display_prob_b1,
            display_prob_b2=display_prob_b2,
            display_prob_damage=display_prob_damage,
            damage_value=damage_value,
            damage_multiplier=rd['damage_multiplier'],
            is_ambiguity=is_ambiguity,
            a_chart_json=json.dumps(a_chart) if a_chart else 'null',
            b_chart_json=json.dumps(b_chart) if b_chart else 'null',
            treatment=treatment,
            kontribusi_text=kontribusi_text,
            min_prob_a1_pct=min_prob_a1_pct,
            min_prob_b1_pct=min_prob_b1_pct,
        )

    def before_next_page(self):
        rd = Constants.rounds_data[self.round_number - 1]
        is_ambiguity = rd['round_type'] == 'ambiguity'
        treatment = self.session.config.get('treatment', 'by_return')

        # Tentukan probabilitas aktual
        if is_ambiguity:
            prob_a1 = self.player.actual_prob_a1
            prob_a2 = self.player.actual_prob_a2
            prob_b1 = self.player.actual_prob_b1
            prob_b2 = self.player.actual_prob_b2
            prob_damage = self.player.actual_prob_damage
        else:
            prob_a1 = rd['prob_a1']
            prob_a2 = rd['prob_a2']
            prob_b1 = rd['prob_b1']
            prob_b2 = rd['prob_b2']
            prob_damage = rd['prob_damage']

        # 1. Tentukan return berdasarkan prospek yang dipilih
        self.player.angka_keluar = random.randint(1, 10000)

        if self.player.prospek_terpilih == 'prospek-A':
            threshold = int(prob_a1 * 10000)
            if self.player.angka_keluar <= threshold:
                self.player.return_multiplier = rd['ret_a1']
            else:
                self.player.return_multiplier = rd['ret_a2']
        else:
            threshold = int(prob_b1 * 10000)
            if self.player.angka_keluar <= threshold:
                self.player.return_multiplier = rd['ret_b1']
            else:
                self.player.return_multiplier = rd['ret_b2']

        self.player.return_token = int(self.player.return_multiplier * rd['investasi'])

        # 2. Cek apakah bencana terjadi
        self.player.angka_damage = random.randint(1, 10000)
        damage_threshold = int(prob_damage * 10000)
        self.player.bencana_terjadi = self.player.angka_damage <= damage_threshold

        # 3. Kalkulasi hasil akhir
        if self.player.bencana_terjadi:
            # Bencana: tidak dapat return
            self.player.return_token = 0
            self.player.kontribusi_token = 0
            self.player.hasil_token = 0
        else:
            # Tidak bencana: hitung kontribusi
            if treatment == 'by_return':
                self.player.kontribusi_token = int(
                    self.player.kontribusi_persen / 100 * self.player.return_token
                )
                self.player.hasil_token = self.player.return_token - self.player.kontribusi_token
            else:
                # By capitalisation: kontribusi dari kapitalisasi, tidak mengurangi payment
                self.player.kontribusi_token = int(
                    self.player.kontribusi_persen / 100 * rd['capital']
                )
                self.player.hasil_token = self.player.return_token


class result(Page):
    def vars_for_template(self):
        rd = Constants.rounds_data[self.round_number - 1]
        is_ambiguity = rd['round_type'] == 'ambiguity'
        treatment = self.session.config.get('treatment', 'by_return')

        # Untuk ambiguity, ungkap probabilitas aktual di result page
        if is_ambiguity:
            actual_prob_a1_pct = round(self.player.actual_prob_a1 * 100, 1)
            actual_prob_a2_pct = round(self.player.actual_prob_a2 * 100, 1)
            actual_prob_b1_pct = round(self.player.actual_prob_b1 * 100, 1)
            actual_prob_b2_pct = round(self.player.actual_prob_b2 * 100, 1)
            actual_prob_damage_pct = round(self.player.actual_prob_damage * 100, 2)
        else:
            actual_prob_a1_pct = int(rd['prob_a1'] * 100)
            actual_prob_a2_pct = int(rd['prob_a2'] * 100)
            actual_prob_b1_pct = int(rd['prob_b1'] * 100)
            actual_prob_b2_pct = int(rd['prob_b2'] * 100)
            actual_prob_damage_pct = int(rd['prob_damage'] * 100)

        def fmt_mult(v):
            if v == int(v):
                return str(int(v))
            return str(v).replace('.', ',')

        ret_a1 = fmt_mult(rd['ret_a1'])
        ret_a2 = f"{int(rd['ret_a2'] * 100)}%"
        ret_b1 = fmt_mult(rd['ret_b1'])
        ret_b2 = f"{int(rd['ret_b2'] * 100)}%"
        # Determine if return is from outcome 1 (x lipat) or outcome 2 (%)
        rm = self.player.return_multiplier
        if self.player.prospek_terpilih == 'prospek-A':
            is_outcome1 = (rm == rd['ret_a1'])
        else:
            is_outcome1 = (rm == rd['ret_b1'])

        if is_outcome1:
            return_mult = fmt_mult(rm) + 'x lipat'
        else:
            return_mult = f"{int(rm * 100)}%"

        return dict(
            round_type=rd['round_type'],
            range_type=rd['range_type'],
            capital=rd['capital'],
            investasi=rd['investasi'],
            cc_inv=rd['cc_inv'],
            ret_a1=ret_a1,
            ret_a2=ret_a2,
            ret_b1=ret_b1,
            ret_b2=ret_b2,
            actual_prob_a1_pct=actual_prob_a1_pct,
            actual_prob_a2_pct=actual_prob_a2_pct,
            actual_prob_b1_pct=actual_prob_b1_pct,
            actual_prob_b2_pct=actual_prob_b2_pct,
            actual_prob_damage_pct=actual_prob_damage_pct,
            damage_value=rd['damage_multiplier'] * rd['investasi'],
            is_ambiguity=is_ambiguity,
            treatment=treatment,
            return_mult=return_mult,
        )


page_sequence = [game, result]
