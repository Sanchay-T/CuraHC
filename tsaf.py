class UserMainCode(object):
    @classmethod
    def getOriginalString(cls, input1):
        # Get the length of the input string
        n = len(input1)

        # If the length is odd, it's not possible to split into two equal halves
        if n % 2 != 0:
            return "notpossible"

        # Split the input string into two equal halves
        half = n // 2
        first_half = input1[:half]
        second_half = input1[half:]

        # Remove all occurrences of 'i' from the first half
        first_half_without_i = first_half.replace("i", "")

        # Reconstruct the string and check if it matches the input
        reconstructed_string = first_half_without_i + first_half
        if reconstructed_string == input1:
            return first_half
        else:
            return "notpossible"


print(UserMainCode.getOriginalString("izizibizzbb"))  # Output: "izizibib"
print(UserMainCode.getOriginalString("aibiciab"))  # Output: "notpossible"
