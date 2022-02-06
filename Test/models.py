from django.db import models


class Respondent(models.Model):
    GENDERS = [(0, 'female'), (1, 'male')]
    id = models.AutoField(primary_key=True)
    age = models.IntegerField()
    gender = models.IntegerField(choices=GENDERS)
    twitter_id = models.CharField(max_length=128)

    def __str__(self):
        return self.twitter_id


class Submit(models.Model):
    MBTI_PERSONALITY_TYPES = [('ESTJ', 'ESTJ'), ('ESTP', 'ESTP'), ('ESFJ', 'ESFJ'), ('ESFP', 'ESFP'),
                              ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
                              ('ISTJ', 'ISTJ'), ('ISTP', 'ISTP'), ('ISFJ', 'ISFJ'), ('ISFP', 'ISFP'),
                              ('INTJ', 'INTJ'), ('INTP', 'INTP'), ('INFJ', 'INFJ'), ('INFP', 'INFP')]

    id = models.AutoField(primary_key=True)
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE, related_name='submits')
    submit_date = models.DateTimeField(auto_now_add=True)
    ptype = models.CharField(choices=MBTI_PERSONALITY_TYPES, max_length=4, blank=True, null=True)

    def update_ptype(self):
        """counts the answers and finds personality type(ptype)
           counting method based on pdf:
           EI questions: 1, 5, 9,...     I answer:1 - E answer:2
           SN questions: 2, 6, 10,...    S answer:1 - N answer:2
           TF questions: 3, 7, 11,...    T answer:1 - F answer:2
           JP questions: 4, 8, 12,...    P answer:1 - J answer:2"""

        if self.answers.all().count() < 60:
            return

        # this array is only for counting answers and is valid only in this method
        #           E  I    N  S    F  T    J  P
        factors = [[0, 0], [0, 0], [0, 0], [0, 0]]
        for answer in self.answers.all():
            factors[(answer.question_num-1) % 4][answer.ans % 2] += 1

        # this array is to find the personality type(ptype) without naested ifs
        types = ['ENFJ', 'ENFP', 'ENTJ', 'ENTP', 'ESFJ', 'ESFP', 'ESTJ', 'ESTP',
                 'INFJ', 'INFP', 'INTJ', 'INTP', 'ISFJ', 'ISFP', 'ISTJ', 'ISTP']

        result_index = 0
        for i in range(len(factors)):
            result_index *= 2
            result_index += 0 if factors[i][0] > factors[i][1] else 1

        self.ptype = types[result_index]
        return

    def save(self, *args, **kwargs):
        self.update_ptype()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.respondent) + " " + str(self.id)


class Answer(models.Model):
    ANSWER_OPTIONS = [(1, '1'), (2, '2'), (0, 'not answered')]

    id = models.AutoField(primary_key=True)
    ans = models.IntegerField(choices=ANSWER_OPTIONS, default=0)
    question_num = models.IntegerField()
    submit = models.ForeignKey(Submit, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.submit.respondent.twitter_id + " " + str(self.question_num)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    option1 = models.CharField(max_length=512)
    option2= models.CharField(max_length=512)
    num = models.IntegerField()

    def __str__(self):
        return "question " + str(self.num)




#
#
# class Test(models.Model):
#     id = models.AutoField(primary_key=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     E = models.IntegerField(default=0)
#     I = models.IntegerField(default=0)
#     S = models.IntegerField(default=0)
#     N = models.IntegerField(default=0)
#     T = models.IntegerField(default=0)
#     F = models.IntegerField(default=0)
#     J = models.IntegerField(default=0)
#     P = models.IntegerField(default=0)
#     PTYPE_CHOICES = [('ESTJ', 'ESTJ'), ('ESTP', 'ESTP'), ('ESFJ', 'ESFJ'), ('ESFP', 'ESFP'),
#                      ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
#                      ('ISTJ', 'ISTJ'), ('ISTP', 'ISTP'), ('ISFJ', 'ISFJ'), ('ISFP', 'ISFP'),
#                      ('INTJ', 'INTJ'), ('INTP', 'INTP'), ('INFJ', 'INFJ'), ('INFP', 'INFP')]
#     ptype = models.CharField(choices=PTYPE_CHOICES)
#     ANSWER_CHOICES = [(0, 'not answered'), (1, '1'), (2, '2')]
#     a1 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a2 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a3 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a4 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a5 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a6 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a7 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a8 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a9 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a10 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a11 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a12 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a13 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a14 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a15 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a16 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a17 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a18 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a19 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a20 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a21 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a22 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a23 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a24 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a25 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a26 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a27 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a28 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a29 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a30 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a31 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a32 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a33 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a34 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a35 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a36 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a37 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a38 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a39 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a40 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a41 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a42 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a43 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a44 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a45 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a46 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a47 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a48 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a49 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a50 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a51 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a52 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a53 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a54 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a55 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a56 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a57 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a58 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a59 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#     a60 = models.IntegerField(default=0, choices=ANSWER_CHOICES)
#
#     EI_answers = [a1, a5, a9, a13, a17, a21, a25, a29, a33, a37, a41, a45, a49, a53, a57]
#     SN_answers = [a2, a6, a10, a14, a18, a22, a26, a30, a34, a38, a42, a46, a50, a54, a58]
#     TF_answers = [a3, a7, a11, a15, a19, a23, a27, a31, a35, a39, a43, a47, a51, a55, a59]
#     JP_answers = [a4, a8, a12, a16, a20, a24, a28, a32, a36, a40, a44, a48, a52, a56, a60]
#
#
#     def update_dems(self):
#         for ans in self.EI_answers:
#             if ans == 1:
#                 self.I += 1
#             elif ans == 2:
#                 self.E += 1
#
#         for ans in self.SN_answers:
#             if ans == 1:
#                 self.S += 1
#             elif ans == 2:
#                 self.N += 1
#
#         for ans in self.TF_answers:
#             if ans == 1:
#                 self.T += 1
#             elif ans == 2:
#                 self.F += 1
#
#         for ans in self.JP_answers:
#             if ans == 1:
#                 self.P += 1
#             elif ans == 2:
#                 self.J += 1
#
#     def update_ptype(self):
#         result = ""
#         result += "E" if self.E > self.I else "I"
#         result += "S" if self.S > self.N else "N"
#         result += "T" if self.T > self.F else "F"
#         result += "J" if self.J > self.P else "P"
#         self.ptype = result
#
#     def save(self, *args, **kwargs):
#         self.update_dems()
#         self.update_ptype()
#         super().save(*args, **kwargs)


