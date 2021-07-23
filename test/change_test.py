from formal_changer import *

informal = '나는 김범관 이다.'
formal = '그랜드 캐년으로 가려면 어느 도시에서 가는 게 제일 쉽습니까?'
# ready model
model = Changer()

# informal to formal
print("formal to informal >>>>>>", model.dechanger(informal))

# formal to informal
print("informal to formal >>>>>>", model.changer(informal))
