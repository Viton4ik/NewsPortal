
from django import template

register = template.Library()

# censorship filter
censorship_list = ['спорт', 'производство', 'согласие', 'рублев', 'углублять', 'example,', 'critical']

@register.filter()
def censor(word):
   word_list_adapted = []
   try:
      word_no_space = word.strip()
      word_list = word_no_space.split()
      for word in word_list:
         word_adapted = word.lower()
         if word_adapted in censorship_list:
            word_censored = word[0] + '*' * (len(word_adapted)-1)
            word_list_adapted.append(word_censored)
         else:
            word_censored = word
            word_list_adapted.append(word_censored)
         corrected = " ".join(word_list_adapted)
      return corrected
   except AttributeError as e:
      return f"ErrorMessage: {e}. Please use only 'str'!"


forbidden_words = ['show', 'international', 'information', 'молдова', 'защиту']
@register.filter()
def forbidden(word):
   word_list_adapted = []
   try:
      word_list = word.strip().split()
      # print(word_list)
      for word in word_list:
        check = True
        while check:
            if word[-1] == '.' or word[-1] == ',':
                word = word[:-1]
            else:
                check = False
        word_adapted = word.lower()
        if word_adapted in forbidden_words:
            word_censored = word[0] + '*' * (len(word_adapted) - 1) + word[-1]
            word_list_adapted.append(word_censored)
        else:
            word_censored = word
            word_list_adapted.append(word_censored)
        corrected = " ".join(word_list_adapted)
      return corrected
   except AttributeError as e:
      return f"ErrorMessage: {e}. Please use only 'str'!"


# multiply filter
@register.filter()
def multiply(var1, var2):
   return var1 * var2

# cash testing filter
@register.filter()
def pow(var1, var2):
   return var1**var2
