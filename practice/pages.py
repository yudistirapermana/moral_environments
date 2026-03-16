from .models import *
import random
import json


# ============================================================
# 1. RISK TASK PRACTICE
# ============================================================
class risk_game(Page):
    form_model = 'player'
    form_fields = ['risk_prospek_terpilih']

    def error_message(self, values):
        if not values.get('risk_prospek_terpilih'):
            return "Silakan pilih salah satu prospek."

    def vars_for_template(self):
        rd = Constants.risk_data

        a_display = []
        for payoff, prob in rd['a_outcomes']:
            a_display.append(dict(
                payoff=payoff,
                prob=prob,
                prob_pct=int(prob * 100),
            ))

        b_display = []
        for payoff, prob in rd['b_outcomes']:
            b_display.append(dict(
                payoff=payoff,
                prob=prob,
                prob_pct=int(prob * 100),
            ))

        a_chart = dict(
            labels=[f"{o['payoff']} token ({o['prob_pct']}%)" for o in a_display],
            data=[o['prob_pct'] for o in a_display],
        )
        b_chart = dict(
            labels=[f"{o['payoff']} token ({o['prob_pct']}%)" for o in b_display],
            data=[o['prob_pct'] for o in b_display],
        )

        return dict(
            a_outcomes=a_display,
            b_outcomes=b_display,
            a_chart_json=json.dumps(a_chart),
            b_chart_json=json.dumps(b_chart),
        )

    def before_next_page(self):
        rd = Constants.risk_data
        self.player.risk_angka_keluar = random.randint(1, 100)

        if self.player.risk_prospek_terpilih == 'prospek-A':
            outcomes = rd['a_outcomes']
        else:
            outcomes = rd['b_outcomes']

        cumulative = 0
        for payoff, prob in outcomes:
            cumulative += int(prob * 100)
            if self.player.risk_angka_keluar <= cumulative:
                self.player.risk_hasil_token = payoff
                break


class risk_result(Page):
    def vars_for_template(self):
        rd = Constants.risk_data

        if self.player.risk_prospek_terpilih == 'prospek-A':
            outcomes = rd['a_outcomes']
        else:
            outcomes = rd['b_outcomes']

        ranges = []
        start = 1
        for payoff, prob in outcomes:
            end = start + int(prob * 100) - 1
            if end >= start:
                ranges.append(dict(start=start, end=end, payoff=payoff))
            start = end + 1

        return dict(outcome_ranges=ranges)


# ============================================================
# 2. AMBIGUITY TASK PRACTICE
# ============================================================
class ambiguity_game(Page):
    form_model = 'player'
    form_fields = ['amb_prospek_terpilih']

    def error_message(self, values):
        if not values.get('amb_prospek_terpilih'):
            return "Silakan pilih salah satu prospek."

    def vars_for_template(self):
        rd = Constants.ambiguity_data
        # Ellsberg: Red=30, sisanya unknown
        display_balls = dict(red=30, yellow=0, blue=0, grey=70)

        return dict(
            round_data=rd,
            choice_type=rd['choice_type'],
            info_text=rd['info_text'],
            display_balls_json=json.dumps(display_balls),
        )

    def before_next_page(self):
        pool = []
        pool.extend(['Merah'] * self.player.amb_comp_red)
        pool.extend(['Kuning'] * self.player.amb_comp_yellow)
        pool.extend(['Biru'] * self.player.amb_comp_blue)

        self.player.amb_bola_keluar = random.choice(pool)

        chosen = self.player.amb_prospek_terpilih
        drawn = self.player.amb_bola_keluar

        # Single color choice
        if drawn == chosen:
            self.player.amb_hasil_token = Constants.ambiguity_payoff_win
        else:
            self.player.amb_hasil_token = 0


class ambiguity_result(Page):
    def vars_for_template(self):
        chosen = self.player.amb_prospek_terpilih
        chosen_display = f"Bola {chosen}"

        color_css_map = {'Merah': 'red', 'Kuning': 'yellow', 'Biru': 'blue'}
        color_text_map = {'Merah': 'text-danger', 'Kuning': 'text-warning', 'Biru': 'text-primary'}

        return dict(
            win=self.player.amb_hasil_token > 0,
            chosen_display=chosen_display,
            drawn_color=self.player.amb_bola_keluar,
            drawn_color_css=color_css_map[self.player.amb_bola_keluar],
            drawn_color_text=color_text_map[self.player.amb_bola_keluar],
            comp_json=json.dumps(dict(
                red=self.player.amb_comp_red,
                yellow=self.player.amb_comp_yellow,
                blue=self.player.amb_comp_blue,
            )),
        )


# ============================================================
# 3. COMPANY TASK PRACTICE
# ============================================================
class company_game(Page):
    form_model = 'player'
    form_fields = ['comp_prospek_terpilih', 'comp_kontribusi_persen']

    def error_message(self, values):
        if not values.get('comp_prospek_terpilih'):
            return "Silakan pilih salah satu prospek investasi."
        if values.get('comp_kontribusi_persen') is None:
            return "Silakan masukkan persentase kontribusi (0-100)."

    def vars_for_template(self):
        rd = Constants.company_data
        treatment = self.session.config.get('treatment', 'by_return')

        display_prob_a1 = f"{int(rd['prob_a1'] * 100)}%"
        display_prob_a2 = f"{int(rd['prob_a2'] * 100)}%"
        display_prob_b1 = f"{int(rd['prob_b1'] * 100)}%"
        display_prob_b2 = f"{int(rd['prob_b2'] * 100)}%"
        display_prob_damage = f"{int(rd['prob_damage'] * 100)}%"

        def fmt_mult(v):
            if v == int(v):
                return str(int(v))
            return str(v).replace('.', ',')

        ret_a1_display = fmt_mult(rd['ret_a1'])
        ret_a2_display = f"{int(rd['ret_a2'] * 100)}%"
        ret_b1_display = fmt_mult(rd['ret_b1'])
        ret_b2_display = f"{int(rd['ret_b2'] * 100)}%"

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

        damage_value = rd['damage_multiplier'] * rd['investasi']

        if treatment == 'by_return':
            kontribusi_text = "dari nilai return yang diperoleh jika tidak terjadi kerusakan lingkungan"
        else:
            kontribusi_text = "dari nilai kapitalisasi perusahaan Anda, terlepas dari ada atau tidaknya kerusakan lingkungan"

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
            is_ambiguity=False,
            a_chart_json=json.dumps(a_chart),
            b_chart_json=json.dumps(b_chart),
            treatment=treatment,
            kontribusi_text=kontribusi_text,
        )

    def before_next_page(self):
        rd = Constants.company_data
        treatment = self.session.config.get('treatment', 'by_return')

        # 1. Tentukan return
        self.player.comp_angka_keluar = random.randint(1, 10000)

        if self.player.comp_prospek_terpilih == 'prospek-A':
            threshold = int(rd['prob_a1'] * 10000)
            if self.player.comp_angka_keluar <= threshold:
                self.player.comp_return_multiplier = rd['ret_a1']
            else:
                self.player.comp_return_multiplier = rd['ret_a2']
        else:
            threshold = int(rd['prob_b1'] * 10000)
            if self.player.comp_angka_keluar <= threshold:
                self.player.comp_return_multiplier = rd['ret_b1']
            else:
                self.player.comp_return_multiplier = rd['ret_b2']

        self.player.comp_return_token = int(self.player.comp_return_multiplier * rd['investasi'])

        # 2. Cek bencana
        self.player.comp_angka_damage = random.randint(1, 10000)
        damage_threshold = int(rd['prob_damage'] * 10000)
        self.player.comp_bencana_terjadi = self.player.comp_angka_damage <= damage_threshold

        # 3. Kalkulasi hasil
        if self.player.comp_bencana_terjadi:
            self.player.comp_return_token = 0
            self.player.comp_kontribusi_token = 0
            self.player.comp_hasil_token = 0
        else:
            if treatment == 'by_return':
                self.player.comp_kontribusi_token = int(
                    self.player.comp_kontribusi_persen / 100 * self.player.comp_return_token
                )
                self.player.comp_hasil_token = self.player.comp_return_token - self.player.comp_kontribusi_token
            else:
                self.player.comp_kontribusi_token = int(
                    self.player.comp_kontribusi_persen / 100 * rd['capital']
                )
                self.player.comp_hasil_token = self.player.comp_return_token


class company_result(Page):
    def vars_for_template(self):
        rd = Constants.company_data
        treatment = self.session.config.get('treatment', 'by_return')

        def fmt_mult(v):
            if v == int(v):
                return str(int(v))
            return str(v).replace('.', ',')

        ret_a1 = fmt_mult(rd['ret_a1'])
        ret_a2 = f"{int(rd['ret_a2'] * 100)}%"
        ret_b1 = fmt_mult(rd['ret_b1'])
        ret_b2 = f"{int(rd['ret_b2'] * 100)}%"

        rm = self.player.comp_return_multiplier
        if self.player.comp_prospek_terpilih == 'prospek-A':
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
            actual_prob_a1_pct=int(rd['prob_a1'] * 100),
            actual_prob_a2_pct=int(rd['prob_a2'] * 100),
            actual_prob_b1_pct=int(rd['prob_b1'] * 100),
            actual_prob_b2_pct=int(rd['prob_b2'] * 100),
            actual_prob_damage_pct=int(rd['prob_damage'] * 100),
            damage_value=rd['damage_multiplier'] * rd['investasi'],
            is_ambiguity=False,
            treatment=treatment,
            return_mult=return_mult,
        )


# ============================================================
# 4. BREAK PAGE (jeda sebelum main task)
# ============================================================
class break_page(Page):
    pass


# ============================================================
# PAGE SEQUENCE
# ============================================================
page_sequence = [
    risk_game,
    risk_result,
    ambiguity_game,
    ambiguity_result,
    company_game,
    company_result,
    break_page,
]
