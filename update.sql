update food_additive
set _10_dangerous_additive='10대 주의성분(발암물질)'
where _name='아질산나트륨';

update food_additive
set _10_dangerous_additive='10대 주의성분(발암물질)'
where _name='카라멜색소';

update food_additive
set _10_dangerous_additive='10대 주의성분(뇌 손상 위험)'
where _name='아스파탐';

update food_additive
set _10_dangerous_additive='10대 주의성분(간, 신장 손상 위험)'
where _name='수크랄로스' or _name='아세설팜칼륨';

update food_additive
set _10_dangerous_additive='10대 주의성분(인간 치사량이 찻숫가락 하나 양)'
where _name='차아염소산나트륨';

update food_additive
set _10_dangerous_additive='10대 주의성분(비타민 C와 결합 시, 백혈병 유발 및 암 유발 가능성 존재)'
where _name='안식향산나트륨';

update food_additive
set _10_dangerous_additive='10대 주의성분(발암물질)'
where _name='사카린나트륨';

