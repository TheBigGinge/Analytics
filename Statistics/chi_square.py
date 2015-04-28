import scipy.stats.mstats as statistics


class ChiSquaredIndependence:
    """
    Chi-Square Test (Test of Independence) designed to function like the one in R.
    R calculates your expected values so I had to add that in.
    Args:
        The observe variable is a list of the viewed observations
        The first two numbers are the frequencies of variable 1
        The second two numbers are the frequencies of variable 2

        Example: Period 1 had 200 conversions and 450 non conversions
        Period 2 had 250 conversions and 400 non conversions

        The variable observe would = [200, 450, 250, 400]

    Returns:
        The output is set. Output[0] = Chi Square Statistic, Output[1] = p_value
    """

    def __init__(self, observations, expected=None):
        self.observe = observations
        self.expected = expected

    def calculate_expected_values(self):

        first_sum = float(self.observe[0] + self.observe[1])
        second_sum = float(self.observe[2] + self.observe[3])
        third_sum = float(self.observe[0] + self.observe[2])
        fourth_sum = float(self.observe[1] + self.observe[3])
        total_sum = float(sum(self.observe))

        exp_one = self.calculate_ratio(first_sum, third_sum, total_sum)
        exp_two = self.calculate_ratio(first_sum, fourth_sum, total_sum)
        exp_three = self.calculate_ratio(second_sum, third_sum, total_sum)
        exp_four = self.calculate_ratio(second_sum, fourth_sum, total_sum)

        observation_list = [exp_one, exp_two, exp_three, exp_four]

        return observation_list

    def calculate_chi_square(self):

        if self.expected is None:
            expected = self.calculate_expected_values()
        else:
            expected = self.expected

        stat_and_p_value = statistics.chisquare(self.observe, f_exp=expected)

        return stat_and_p_value

    @staticmethod
    def calculate_ratio(first_obs, second_obs, total_sum):
        try:
            exp = (first_obs * second_obs) / total_sum
        except ZeroDivisionError:
            exp = 0

        return exp


class ChiSquaredGoodnessOfFit:

    def __init__(self, observations, expected_frequencies):
        self.observations = observations
        self.expected_frequencies = expected_frequencies

    def calculate_expected_values(self):

        expected_values = []

        for i, value in enumerate(self.observations):

            expected_value = self.observations[i] * self.expected_frequencies[i]
            expected_values.append(expected_value)

        return expected_values

    def calculate_chi_square(self):

        expected_values = self.calculate_expected_values()

        stat_and_p_value = statistics.chisquare(self.observations, f_exp=expected_values)

        return stat_and_p_value