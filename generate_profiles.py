import os

# Complete Dreamgrove base profile
FULL_PROFILE = """
druid="tauren"
source=default
spec=balance
level=90
race=tauren
role=spell
position=back
professions=leatherworking=100/jewelcrafting=100
talents=CYGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWoMbNMmZgxsMzMzMLMgxMLzwYGLsMzyMjxMbYAwYbZmBjZbEYCAAAwCzMzMYzYGjZAAMzglBA
omnium_talents=136822:1/136819:1/136817:1/136815:1/136814:1

# Default consumables
potion=potion_of_recklessness_2
flask=flask_of_the_shattered_sun_2
food=silvermoon_parade
augmentation=void_touched
temporary_enchant=main_hand:thalassian_phoenix_oil_2

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=snapshot_stats
actions.precombat+=/variable,name=no_cd_talent,value=!talent.celestial_alignment&!talent.incarnation_chosen_of_elune|druid.no_cds
actions.precombat+=/variable,name=anchor_cd,value=hero_tree.keeper_of_the_grove&talent.force_of_nature|hero_tree.elunes_chosen&talent.fury_of_elune&!talent.lunation
actions.precombat+=/variable,name=opener,value=1
actions.precombat+=/variable,name=on_use_trinket,value=0
actions.precombat+=/variable,name=on_use_trinket,op=add,value=trinket.1.has_use_buff
actions.precombat+=/variable,name=on_use_trinket,op=add,value=(trinket.2.has_use_buff)*2
actions.precombat+=/variable,name=prio,value=0
actions.precombat+=/moonkin_form
actions.precombat+=/wrath
actions.precombat+=/wrath
actions.precombat+=/wrath,if=hero_tree.keeper_of_the_grove&enemies=1
actions.precombat+=/starfire,if=hero_tree.elunes_chosen|enemies>1

# Executed every time the actor is available.
actions=variable,name=passive_asp,value=(2+2*set_bonus.mid1_2pc*buff.eclipse.down)*(dot.moonfire.ticking+dot.sunfire.ticking+buff.solstice.up*((active_dot.moonfire_dmg>4)+(active_dot.moonfire_dmg>16)+(active_dot.sunfire_dmg>4)+(active_dot.sunfire_dmg>16)))%spell_haste+talent.natures_balance+buff.fury_of_elune.up*((floor(buff.fury_of_elune.remains%0.5)>?4)*2.5+talent.the_eternal_moon*(buff.fury_of_elune.remains<2)*6)+buff.sundered_firmament.up*((floor(buff.sundered_firmament.remains%0.5)>?4)*0.6+talent.the_eternal_moon*(buff.sundered_firmament.remains<2)*6)
actions+=/variable,name=starsurge_cost,value=action.starsurge.base_cost-buff.astral_communion.up*15-talent.elunes_guidance*buff.incarnation_chosen_of_elune.up*10
actions+=/variable,name=starfall_cost,value=action.starfall.base_cost-buff.astral_communion.up*15-talent.elunes_guidance*buff.incarnation_chosen_of_elune.up*12
actions+=/variable,name=ca_pooling_threshold,value=(action.starsurge.base_cost-talent.incarnation_chosen_of_elune*talent.elunes_guidance*10)*(3-buff.touch_the_cosmos.react-buff.starweavers_weft.react-buff.starweavers_warp.react)-talent.astral_communion*15>?astral_power.max-20
actions+=/variable,name=ecl_pooling_threshold,value=action.starsurge.base_cost*(3-buff.touch_the_cosmos.react-buff.starweavers_weft.react-buff.starweavers_warp.react)-talent.astral_communion*15>?astral_power.max
actions+=/variable,name=ca_control_remains,value=cooldown.ca_inc.full_recharge_time+cooldown.ca_inc.duration-(cooldown.ca_inc.base_duration-talent.control_of_the_dream*15)
actions+=/variable,name=convoke_control_remains,value=cooldown.convoke_the_spirits.remains+cooldown.convoke_the_spirits.duration-(cooldown.convoke_the_spirits.base_duration-talent.control_of_the_dream*15)
actions+=/variable,name=fon_control_remains,value=cooldown.force_of_nature.remains+cooldown.force_of_nature.duration-(cooldown.force_of_nature.base_duration-talent.control_of_the_dream*15)
actions+=/variable,name=next_on_use_trinket_remains,value=(variable.on_use_trinket=1)*trinket.1.cooldown.remains+(variable.on_use_trinket=2)*trinket.2.cooldown.remains+(variable.on_use_trinket=3)*(trinket.1.cooldown.remains>?trinket.2.cooldown.remains)
actions+=/variable,name=anchor_cd_duration,value=variable.anchor_cd*(hero_tree.keeper_of_the_grove*cooldown.force_of_nature.duration<?hero_tree.elunes_chosen*cooldown.fury_of_elune.duration)
actions+=/variable,name=anchor_cd_remains,value=variable.anchor_cd*(hero_tree.keeper_of_the_grove*cooldown.force_of_nature.remains<?hero_tree.elunes_chosen*cooldown.fury_of_elune.remains)
actions+=/variable,name=anchor_cd_hold_remains,value=variable.anchor_cd*(variable.anchor_cd_remains<?hero_tree.keeper_of_the_grove*variable.fon_control_remains)
actions+=/variable,name=cds_synced,value=hero_tree.keeper_of_the_grove&talent.fury_of_elune&(cooldown.fury_of_elune.remains>cooldown.force_of_nature.remains-5&cooldown.fury_of_elune.remains<variable.fon_control_remains+5)
actions+=/variable,name=ca_burst_effective_cd,value=variable.cds_synced*cooldown.fury_of_elune.remains<?variable.anchor_cd_remains-variable.cds_synced*gcd.max<?cooldown.ca_inc.remains-(variable.anchor_cd+variable.cds_synced)*gcd.max<?(cooldown.convoke_the_spirits.remains+action.convoke_the_spirits.execute_time+gcd.max-10-variable.cds_synced*gcd.max)*(!variable.anchor_cd|cooldown.convoke_the_spirits.remains<variable.anchor_cd_hold_remains+10)*(cooldown.convoke_the_spirits.remains<variable.ca_control_remains)
actions+=/variable,name=ca_burst_hold_remains,value=(variable.cds_synced*(cooldown.fury_of_elune.remains+5>?variable.fon_control_remains-gcd.max)+!variable.cds_synced*(variable.anchor_cd_hold_remains+!variable.anchor_cd*fight_remains)>?variable.ca_control_remains-(variable.anchor_cd+variable.cds_synced)*gcd.max>?talent.convoke_the_spirits*(variable.convoke_control_remains-(1+variable.anchor_cd+variable.cds_synced)*gcd.max)+!talent.convoke_the_spirits*fight_remains)<?variable.ca_burst_effective_cd
actions+=/variable,name=ecl_burst_effective_cd,value=variable.cds_synced*cooldown.fury_of_elune.remains<?variable.anchor_cd_remains-variable.cds_synced*gcd.max<?(cooldown.eclipse.remains<?buff.eclipse.remains)-(variable.anchor_cd+variable.cds_synced)*gcd.max<?(cooldown.convoke_the_spirits.remains+action.convoke_the_spirits.execute_time+gcd.max-10-variable.cds_synced*gcd.max)*(!variable.anchor_cd|cooldown.convoke_the_spirits.remains<variable.anchor_cd_hold_remains+10)
actions+=/variable,name=ecl_burst_hold_remains,value=(variable.cds_synced*(cooldown.fury_of_elune.remains+5>?variable.fon_control_remains-gcd.max)+!variable.cds_synced*(variable.anchor_cd_hold_remains+!variable.anchor_cd*fight_remains)>?talent.convoke_the_spirits*(variable.convoke_control_remains-(1+variable.anchor_cd+variable.cds_synced)*gcd.max)+!talent.convoke_the_spirits*fight_remains)<?0
actions+=/variable,name=ca_burst_effective_cd,op=max,value=variable.next_on_use_trinket_remains-(variable.anchor_cd+variable.cds_synced)*gcd.max,if=variable.on_use_trinket&(variable.ca_burst_hold_remains+5>=variable.next_on_use_trinket_remains-(variable.anchor_cd+variable.cds_synced)*gcd.max|cooldown.ca_inc.full_recharge_time>(variable.next_on_use_trinket_remains<?(variable.ecl_burst_effective_cd<?variable.ecl_burst_hold_remains)+variable.anchor_cd_duration+talent.control_of_the_dream*((15-variable.fon_control_remains<?0)+(variable.fon_control_remains-(variable.ecl_burst_effective_cd<?variable.ecl_burst_hold_remains)-variable.cds_synced*gcd.max<?0))+(variable.anchor_cd+variable.cds_synced)*gcd.max))&fight_remains>variable.next_on_use_trinket_remains+buff.ca_inc.duration+gcd.max&(!talent.convoke_the_spirits|variable.ca_burst_effective_cd>=(cooldown.convoke_the_spirits.remains+action.convoke_the_spirits.execute_time+gcd.max-10-variable.cds_synced*gcd.max)|variable.convoke_control_remains>variable.next_on_use_trinket_remains+(variable.on_use_trinket=1)*trinket.1.cooldown.duration+(variable.on_use_trinket=2)*trinket.2.cooldown.duration+(variable.on_use_trinket=3)*((trinket.1.cooldown.remains>=trinket.2.cooldown.remains)*trinket.1.cooldown.remains+(trinket.1.cooldown.remains<trinket.2.cooldown.remains)*trinket.2.cooldown.remains<?20))&(variable.anchor_cd|talent.convoke_the_spirits|variable.on_use_trinket=3|!cooldown.ca_inc.ready|cooldown.ca_inc.base_duration>(variable.on_use_trinket=1)*trinket.1.cooldown.duration+(variable.on_use_trinket=2)*trinket.2.cooldown.duration)
actions+=/variable,name=ca_burst_effective_cd,op=max,value=cooldown.potion.remains-(variable.anchor_cd+variable.cds_synced)*gcd.max,if=((variable.anchor_cd|talent.convoke_the_spirits)&variable.ca_burst_hold_remains>=cooldown.potion.remains-(variable.anchor_cd+variable.cds_synced)*gcd.max|fight_remains<(cooldown.ca_inc.full_recharge_time<?(talent.convoke_the_spirits&!talent.elunes_guidance)*(variable.convoke_control_remains+cooldown.convoke_the_spirits.base_duration-talent.control_of_the_dream*15))+!(talent.convoke_the_spirits&!talent.elunes_guidance)*buff.ca_inc.duration+(talent.convoke_the_spirits&!talent.elunes_guidance)*action.convoke_the_spirits.execute_time+gcd.max)&fight_remains>cooldown.potion.remains+buff.ca_inc.duration+5&cooldown.ca_inc.remains<cooldown.potion.remains
actions+=/variable,name=ecl_burst_effective_cd,op=max,value=variable.next_on_use_trinket_remains-(variable.anchor_cd+variable.cds_synced)*gcd.max,if=variable.on_use_trinket&(variable.ecl_burst_hold_remains<cooldown.ca_inc.remains|variable.ecl_burst_hold_remains>=cooldown.ca_inc.remains&(variable.ca_burst_effective_cd~=variable.next_on_use_trinket_remains-(variable.anchor_cd+variable.cds_synced)*gcd.max|variable.ca_burst_hold_remains>=variable.ca_burst_effective_cd))&variable.ecl_burst_hold_remains+5>=variable.next_on_use_trinket_remains-(variable.anchor_cd+variable.cds_synced)*gcd.max&fight_remains>variable.next_on_use_trinket_remains+buff.eclipse.duration+gcd.max
actions+=/variable,name=ca_burst_hold_remains,op=max,value=variable.ca_burst_effective_cd
actions+=/variable,name=ecl_burst_hold_remains,op=max,value=variable.ecl_burst_effective_cd
actions+=/variable,name=pre_burst_condition,op=reset,if=prev.incarnation_chosen_of_elune|prev.celestial_alignment|!variable.ca_burst_next&(prev.solar_eclipse|prev.lunar_eclipse)
actions+=/variable,name=ca_burst_next,default=1,value=variable.ca_burst_effective_cd~<=variable.ecl_burst_hold_remains&((((variable.ca_burst_effective_cd+(variable.anchor_cd+variable.cds_synced)*gcd.max<?(buff.eclipse.remains<?cooldown.eclipse.remains)+buff.eclipse.duration+gcd.max)+buff.ca_inc.duration)~<=(variable.ca_burst_hold_remains+buff.ca_inc.duration+(variable.anchor_cd+variable.cds_synced)*gcd.max>?(buff.eclipse.remains<?cooldown.eclipse.full_recharge_time)+cooldown.eclipse.duration+gcd.max))|((variable.ca_burst_effective_cd+(variable.anchor_cd+variable.cds_synced)*gcd.max<?((buff.eclipse.remains<?cooldown.eclipse.remains)+buff.eclipse.duration+gcd.max<?cooldown.eclipse.full_recharge_time)+buff.eclipse.duration)+buff.ca_inc.duration~<=(variable.ca_burst_hold_remains+buff.ca_inc.duration+(variable.anchor_cd+variable.cds_synced)*gcd.max>?(buff.eclipse.remains<?cooldown.eclipse.full_recharge_time)+(cooldown.eclipse.duration+gcd.max)*2)))|!(variable.anchor_cd|talent.convoke_the_spirits)|variable.ca_control_remains<variable.ecl_burst_hold_remains+variable.anchor_cd_duration+talent.control_of_the_dream*((15-variable.fon_control_remains<?0)+(variable.fon_control_remains-variable.ecl_burst_hold_remains-variable.cds_synced*gcd.max<?0))+(1+variable.anchor_cd+variable.cds_synced)*gcd.max|fight_remains<variable.anchor_cd_remains+variable.anchor_cd_duration+10&fight_remains>variable.ca_burst_effective_cd+10|fight_remains<(cooldown.ca_inc.full_recharge_time<?(talent.convoke_the_spirits&!talent.elunes_guidance)*(variable.convoke_control_remains+cooldown.convoke_the_spirits.base_duration-talent.control_of_the_dream*15))+!(talent.convoke_the_spirits&!talent.elunes_guidance)*buff.ca_inc.duration+(talent.convoke_the_spirits&!talent.elunes_guidance)*action.convoke_the_spirits.execute_time+gcd.max&fight_remains>cooldown.potion.remains+buff.ca_inc.duration+5&cooldown.ca_inc.remains<cooldown.potion.remains&!(variable.ecl_burst_hold_remains>cooldown.eclipse.full_recharge_time+(1-variable.anchor_cd-variable.cds_synced)*gcd.max|variable.ecl_burst_effective_cd<cooldown.eclipse.full_recharge_time-buff.eclipse.duration-(1+variable.anchor_cd-variable.cds_synced)*gcd.max),if=!variable.ecl_counter&(prev.incarnation_chosen_of_elune|prev.celestial_alignment|!variable.opener&(prev.solar_eclipse|prev.lunar_eclipse))|prev.convoke_the_spirits
actions+=/variable,name=burst_hold_remains,value=variable.ca_burst_next*variable.ca_burst_hold_remains<?!variable.ca_burst_next*variable.ecl_burst_hold_remains
actions+=/variable,name=burst_effective_cd,value=variable.ca_burst_next*variable.ca_burst_effective_cd<?!variable.ca_burst_next*variable.ecl_burst_effective_cd
actions+=/variable,name=burst_hold_remains,op=min,value=variable.burst_effective_cd<?variable.next_on_use_trinket_remains,if=variable.on_use_trinket&!(variable.anchor_cd|talent.convoke_the_spirits)
actions+=/variable,name=burst_hold_remains,op=min,value=variable.burst_effective_cd<?fight_remains-((variable.ca_burst_next*buff.ca_inc.duration+!variable.ca_burst_next*buff.eclipse.duration<?(fight_remains-cooldown.potion.remains>?30))+(1+variable.anchor_cd+variable.cds_synced)*gcd.max)
actions+=/variable,name=ecl_counter,op=add,value=1,if=prev.incarnation_chosen_of_elune|prev.celestial_alignment|!variable.opener&(prev.solar_eclipse|prev.lunar_eclipse)
actions+=/variable,name=ecl_before_burst,value=variable.burst_hold_remains>((!cooldown.eclipse.ready*(cooldown.eclipse.remains+gcd.max)<?buff.eclipse.remains+gcd.max)+buff.eclipse.duration<?!variable.ca_burst_next*(cooldown.eclipse.full_recharge_time+gcd.max+(variable.ecl_counter>1)*5))-(variable.anchor_cd+variable.cds_synced)*gcd.max,if=prev.incarnation_chosen_of_elune|prev.celestial_alignment|prev.solar_eclipse|prev.lunar_eclipse|prev.convoke_the_spirits
actions+=/variable,name=double_ecl_before_burst,value=variable.burst_hold_remains>((!cooldown.eclipse.ready*(cooldown.eclipse.remains+gcd.max)<?buff.eclipse.remains+gcd.max)+buff.eclipse.duration<?cooldown.eclipse.full_recharge_time)+buff.eclipse.duration+(1-variable.anchor_cd-variable.cds_synced)*gcd.max&(variable.ca_burst_next|variable.ecl_burst_hold_remains>cooldown.eclipse.full_recharge_time+cooldown.eclipse.duration+(1-variable.anchor_cd-variable.cds_synced)*gcd.max+5),if=prev.incarnation_chosen_of_elune|prev.celestial_alignment|prev.solar_eclipse|prev.lunar_eclipse|prev.convoke_the_spirits
actions+=/variable,name=burst_refresh_moonfire,value=(hero_tree.elunes_chosen|!talent.treants_of_the_moon|!variable.anchor_cd)&dot.moonfire.remains<10+(variable.anchor_cd+variable.cds_synced)*gcd.max
actions+=/variable,name=burst_refresh_sunfire,value=dot.sunfire.remains<10+(variable.anchor_cd+variable.cds_synced+hero_tree.keeper_of_the_grove*talent.wild_mushroom*cooldown.wild_mushroom.charges)*gcd.max
actions+=/variable,name=burst_pooling_threshold,value=((!(talent.convoke_the_spirits&variable.cds_synced&variable.burst_effective_cd>=cooldown.convoke_the_spirits.remains+action.convoke_the_spirits.execute_time+gcd.max-10-variable.cds_synced*gcd.max)*astral_power.max<?(action.starsurge.base_cost-(variable.ca_burst_next&talent.incarnation_chosen_of_elune&talent.elunes_guidance)*10)*3-talent.astral_communion*15)>?astral_power.max)-(action.starsurge.base_cost-(variable.ca_burst_next&talent.incarnation_chosen_of_elune&talent.elunes_guidance)*10)*(buff.touch_the_cosmos.react+buff.starweavers_weft.react+buff.starweavers_warp.react)-variable.passive_asp-variable.anchor_cd*(hero_tree.keeper_of_the_grove*action.force_of_nature.energize_amount<?hero_tree.elunes_chosen*15)-variable.cds_synced*15-variable.burst_refresh_moonfire*action.moonfire.energize_amount-variable.burst_refresh_sunfire*action.sunfire.energize_amount-hero_tree.keeper_of_the_grove*talent.wild_mushroom*cooldown.wild_mushroom.charges*action.wild_mushroom.energize_amount
actions+=/variable,name=pre_burst_condition,value=variable.burst_effective_cd<=(variable.burst_refresh_moonfire+variable.burst_refresh_sunfire+hero_tree.keeper_of_the_grove*talent.wild_mushroom*cooldown.wild_mushroom.charges)*gcd.max&buff.eclipse.remains<=(variable.anchor_cd+variable.cds_synced+variable.burst_refresh_moonfire+variable.burst_refresh_sunfire+hero_tree.keeper_of_the_grove*talent.wild_mushroom*cooldown.wild_mushroom.charges)*gcd.max&(cooldown.eclipse.full_recharge_time>=buff.ca_inc.duration+(variable.anchor_cd+variable.cds_synced+variable.burst_refresh_moonfire+variable.burst_refresh_sunfire+hero_tree.keeper_of_the_grove*talent.wild_mushroom*cooldown.wild_mushroom.charges)*gcd.max&variable.ecl_counter>2|!variable.ca_burst_next|!variable.ecl_before_burst)&(astral_power>=variable.burst_pooling_threshold|(variable.burst_hold_remains>?cooldown.eclipse.full_recharge_time-(variable.anchor_cd+variable.cds_synced)*gcd.max)<(1+variable.burst_refresh_moonfire+variable.burst_refresh_sunfire+hero_tree.keeper_of_the_grove*talent.wild_mushroom*cooldown.wild_mushroom.charges)*gcd.max),if=!variable.pre_burst_condition
actions+=/variable,name=ecl_counter,op=reset,if=!variable.opener&variable.pre_burst_condition
actions+=/use_items,if=!variable.opener&(variable.anchor_cd&(hero_tree.keeper_of_the_grove&prev_gcd.1.force_of_nature|hero_tree.elunes_chosen&prev_gcd.1.fury_of_elune)|!variable.anchor_cd&variable.pre_burst_condition&!variable.burst_refresh_moonfire&!variable.burst_refresh_sunfire)&(variable.ca_burst_next&cooldown.ca_inc.ready|!cooldown.ca_inc.ready|variable.on_use_trinket=3&(!trinket.1.cooldown.ready&(trinket.1.cooldown.remains<?20)<=(cooldown.potion.remains<?variable.anchor_cd_hold_remains+gcd.max)+5|trinket.1.cooldown.ready&(trinket.2.cooldown.remains<?20)<=(cooldown.potion.remains<?variable.anchor_cd_hold_remains+gcd.max)+5)|fight_remains>(trinket.1.cooldown.ready*trinket.1.cooldown.duration<?trinket.2.cooldown.ready*trinket.2.cooldown.duration)+15)|buff.ca_inc.up&fight_remains<cooldown.ca_inc.remains|buff.eclipse.up&fight_remains<(cooldown.ca_inc.remains>?variable.anchor_cd_remains)+10|fight_remains<15+gcd.max
actions+=/potion,if=!variable.opener&(variable.anchor_cd&(hero_tree.keeper_of_the_grove&prev_gcd.1.force_of_nature|hero_tree.elunes_chosen&prev_gcd.1.fury_of_elune)|!variable.anchor_cd&variable.pre_burst_condition&!variable.burst_refresh_moonfire&!variable.burst_refresh_sunfire)&(variable.ca_burst_next&cooldown.ca_inc.ready|fight_remains<(cooldown.ca_inc.remains>?variable.anchor_cd_remains)+10)|buff.ca_inc.up&fight_remains<cooldown.ca_inc.remains|buff.eclipse.up&fight_remains<(cooldown.ca_inc.remains>?variable.anchor_cd_remains)+10|fight_remains<30+gcd.max
actions+=/berserking,if=!variable.opener&(variable.anchor_cd&(hero_tree.keeper_of_the_grove&prev_gcd.1.force_of_nature|hero_tree.elunes_chosen&prev_gcd.1.fury_of_elune)|!variable.anchor_cd&variable.pre_burst_condition&!variable.burst_refresh_moonfire&!variable.burst_refresh_sunfire)|buff.ca_inc.up&fight_remains<cooldown.ca_inc.remains|buff.eclipse.up&fight_remains<(cooldown.ca_inc.remains>?variable.anchor_cd_remains)+10|fight_remains<buff.berserking.duration+gcd.max
actions+=/invoke_external_buff,name=power_infusion,if=!variable.opener&(variable.anchor_cd&(hero_tree.keeper_of_the_grove&prev_gcd.1.force_of_nature|hero_tree.elunes_chosen&prev_gcd.1.fury_of_elune)|!variable.anchor_cd&variable.pre_burst_condition&!variable.burst_refresh_moonfire&!variable.burst_refresh_sunfire)|buff.ca_inc.up&fight_remains<cooldown.ca_inc.remains|buff.eclipse.up&fight_remains<(cooldown.ca_inc.remains>?variable.anchor_cd_remains)+10|fight_remains<buff.power_infusion.duration+gcd.max
actions+=/run_action_list,name=ec_st,if=hero_tree.elunes_chosen
actions+=/run_action_list,name=kotg_st

actions.ec_st=variable,name=opener,op=reset,if=buff.ca_inc.up
actions.ec_st+=/run_action_list,name=ec_st_opener,if=variable.opener
actions.ec_st+=/celestial_alignment,add_queue_lag=1,if=variable.anchor_cd&prev_gcd.1.fury_of_elune&variable.ca_burst_next
actions.ec_st+=/lunar_eclipse,if=variable.anchor_cd&prev_gcd.1.fury_of_elune
actions.ec_st+=/moonfire,target_if=remains<(gcd.max>?fight_remains)|buff.eclipse.down&refreshable|variable.pre_burst_condition&variable.burst_refresh_moonfire
actions.ec_st+=/sunfire,target_if=remains<(gcd.max>?fight_remains)|buff.eclipse.down&refreshable|variable.pre_burst_condition&variable.burst_refresh_sunfire
actions.ec_st+=/fury_of_elune,if=variable.pre_burst_condition|talent.lunation|buff.ca_inc.up|fight_remains<(fight_remains<cooldown.ca_inc.remains+gcd.max)*variable.burst_hold_remains+buff.fury_of_elune.duration+gcd.max
actions.ec_st+=/celestial_alignment,add_queue_lag=1,if=!variable.anchor_cd&variable.pre_burst_condition&variable.ca_burst_next
actions.ec_st+=/lunar_eclipse,if=!variable.anchor_cd&variable.pre_burst_condition
actions.ec_st+=/lunar_eclipse,if=variable.ecl_before_burst&cooldown.eclipse.full_recharge_time<gcd.max
actions.ec_st+=/lunar_eclipse,if=variable.ecl_before_burst&(astral_power>variable.ecl_pooling_threshold|astral_power.deficit<action.starfire.energize_amount+variable.passive_asp)
actions.ec_st+=/lunar_eclipse,if=variable.ecl_before_burst&variable.burst_hold_remains<0.5+buff.starlord.duration+(1-variable.anchor_cd)*gcd.max|variable.double_ecl_before_burst&variable.burst_hold_remains<(variable.burst_hold_remains-cooldown.eclipse.full_recharge_time>?0.5+buff.starlord.duration+(1-variable.anchor_cd)*gcd.max)+!buff.starlord.at_max_stacks*(0.5+buff.starlord.duration+gcd.max)+buff.starlord.at_max_stacks*(buff.eclipse.duration+gcd.max)
actions.ec_st+=/lunar_eclipse,if=fight_remains<buff.eclipse.duration+gcd.max+(((fight_remains-cooldown.ca_inc.remains<?0)<?(fight_remains-(cooldown.eclipse.full_recharge_time<?buff.eclipse.duration)<?0))>?((fight_remains-cooldown.ca_inc.remains<?0)>?buff.ca_inc.duration+gcd.max)+((fight_remains-(cooldown.eclipse.full_recharge_time<?buff.eclipse.duration)<?0)>?buff.eclipse.duration+gcd.max))
actions.ec_st+=/fury_of_elune,if=cooldown.ca_inc.remains<gcd.max&(buff.eclipse.remains<gcd.max&fight_remains<buff.ca_inc.duration+gcd.max*2+((fight_remains-cooldown.eclipse.remains<?0)>?buff.eclipse.duration+gcd.max)|fight_remains<buff.ca_inc.duration+gcd.max*2)
actions.ec_st+=/celestial_alignment,add_queue_lag=1,if=buff.eclipse.down&fight_remains<buff.ca_inc.duration+gcd.max+((fight_remains-cooldown.eclipse.remains<?0)>?buff.eclipse.duration+gcd.max)|fight_remains<buff.ca_inc.duration+gcd.max
actions.ec_st+=/convoke_the_spirits,if=(time-action.fury_of_elune.last_used<10)&buff.eclipse.up&(astral_power<variable.starsurge_cost|(buff.touch_the_cosmos.react|buff.starweavers_warp.react|buff.starweavers_weft.react)&astral_power.deficit>60|buff.eclipse.remains<execute_time+gcd.max)&(fight_remains>cooldown.convoke_the_spirits.duration+execute_time|buff.ca_inc.up|fight_remains<cooldown.ca_inc.remains+execute_time+gcd.max)|(buff.ca_inc.up|buff.eclipse.up&fight_remains<cooldown.ca_inc.remains+execute_time+gcd.max)&(astral_power<variable.starsurge_cost|(buff.touch_the_cosmos.up|buff.starweavers_warp.up|buff.starweavers_weft.up)&astral_power.deficit>60|buff.eclipse.remains<execute_time+gcd.max)|fight_remains<execute_time+gcd.max
actions.ec_st+=/starfall,if=buff.starweavers_warp.react
actions.ec_st+=/starfall,if=(talent.starweaver&(buff.ca_inc.down&talent.meteorites&talent.stellar_amplification&(talent.aetherial_kindling|!talent.power_of_goldrinn)|buff.eclipse.down&(talent.meteorites|talent.aetherial_kindling|talent.stellar_amplification&!talent.power_of_goldrinn))|buff.ca_inc.down&talent.incarnation_chosen_of_elune&talent.meteorites&talent.stellar_amplification&talent.aetherial_kindling&!talent.power_of_goldrinn|buff.eclipse.down&(talent.meteorites|talent.incarnation_chosen_of_elune&talent.aetherial_kindling))&buff.touch_the_cosmos.react&!buff.starweavers_weft.react
actions.ec_st+=/starsurge,if=buff.touch_the_cosmos.react|buff.starweavers_weft.react
actions.ec_st+=/starsurge,if=buff.eclipse.up&(buff.touch_the_cosmos.react|buff.starweavers_weft.react|astral_power>=variable.starsurge_cost*(1+(buff.incarnation_chosen_of_elune.down&buff.ascendant_stars.down&buff.eclipse.remains<5))&(buff.ascendant_stars.up|variable.burst_hold_remains>5))
actions.ec_st+=/starsurge,if=buff.eclipse.down&!buff.starlord.at_max_stacks&(variable.ecl_before_burst&!cooldown.eclipse.ready&variable.burst_hold_remains>30|!variable.ecl_before_burst&variable.burst_hold_remains>10)&astral_power>=variable.starsurge_cost
actions.ec_st+=/starsurge,if=variable.burst_hold_remains>gcd.max*2&astral_power.deficit<action.starfire.energize_amount+variable.passive_asp
actions.ec_st+=/new_moon,if=astral_power.deficit>energize_amount
actions.ec_st+=/half_moon,if=astral_power.deficit>energize_amount
actions.ec_st+=/full_moon,if=astral_power.deficit>energize_amount
actions.ec_st+=/starfire

actions.ec_st_opener=moonfire,if=last_used<0
actions.ec_st_opener+=/sunfire,if=last_used<0
actions.ec_st_opener+=/fury_of_elune,if=talent.lunation
actions.ec_st_opener+=/potion
actions.ec_st_opener+=/eclipse,if=last_used<0
actions.ec_st_opener+=/starfall,if=buff.starweavers_warp.react&(buff.ascendant_stars.up|astral_power<variable.burst_pooling_threshold)
actions.ec_st_opener+=/starsurge,if=(buff.touch_the_cosmos.react|buff.starweavers_weft.react)&(buff.ascendant_stars.stack>talent.convoke_the_spirits|astral_power<variable.burst_pooling_threshold)|buff.ascendant_stars.stack>talent.convoke_the_spirits&astral_power>=variable.starsurge_cost
actions.ec_st_opener+=/starfire,if=astral_power<variable.burst_pooling_threshold
actions.ec_st_opener+=/moonfire,if=variable.burst_refresh_moonfire&variable.ca_burst_effective_cd=0
actions.ec_st_opener+=/sunfire,if=variable.burst_refresh_sunfire&variable.ca_burst_effective_cd=0
actions.ec_st_opener+=/fury_of_elune
actions.ec_st_opener+=/use_items,check_existing=0
actions.ec_st_opener+=/berserking
actions.ec_st_opener+=/invoke_external_buff,name=power_infusion
actions.ec_st_opener+=/celestial_alignment,add_queue_lag=1

actions.kotg_st=variable,name=opener,op=reset,if=buff.ca_inc.up
actions.kotg_st+=/run_action_list,name=kotg_st_opener,if=variable.opener
actions.kotg_st+=/celestial_alignment,add_queue_lag=1,if=prev_gcd.1.force_of_nature&variable.ca_burst_next
actions.kotg_st+=/solar_eclipse,if=prev_gcd.1.force_of_nature
actions.kotg_st+=/moonfire,target_if=remains<(gcd.max>?fight_remains)&(!talent.treants_of_the_moon|cooldown.force_of_nature.remains>3&buff.harmony_of_the_grove.down)|(!ticking|buff.eclipse.down&refreshable)&(!talent.treants_of_the_moon|buff.harmony_of_the_grove.down)
actions.kotg_st+=/sunfire,target_if=remains<(gcd.max>?fight_remains)|buff.eclipse.down&buff.harmony_of_the_grove.down&refreshable|variable.pre_burst_condition&variable.burst_refresh_sunfire&!(talent.wild_mushroom&cooldown.wild_mushroom.charges)
actions.kotg_st+=/wild_mushroom,if=variable.pre_burst_condition
actions.kotg_st+=/fury_of_elune,if=variable.pre_burst_condition|!variable.cds_synced|buff.ca_inc.up|fight_remains<(fight_remains<cooldown.ca_inc.remains+gcd.max)*variable.burst_hold_remains+buff.fury_of_elune.duration+gcd.max
actions.kotg_st+=/force_of_nature,if=variable.pre_burst_condition&!variable.cds_synced|buff.ca_inc.up|fight_remains<(fight_remains<cooldown.ca_inc.remains+gcd.max)*variable.burst_hold_remains+buff.harmony_of_the_grove.duration+(1+variable.cds_synced)*gcd.max
actions.kotg_st+=/solar_eclipse,if=variable.ecl_before_burst&cooldown.eclipse.full_recharge_time<gcd.max
actions.kotg_st+=/solar_eclipse,if=variable.ecl_before_burst&(astral_power>variable.ecl_pooling_threshold|astral_power.deficit<action.wrath.energize_amount+variable.passive_asp)
actions.kotg_st+=/solar_eclipse,if=variable.ecl_before_burst&variable.burst_hold_remains<0.5+buff.starlord.duration+(1-variable.anchor_cd-variable.cds_synced)*gcd.max|variable.double_ecl_before_burst&variable.burst_hold_remains<(variable.burst_hold_remains-cooldown.eclipse.full_recharge_time>?0.5+buff.starlord.duration+(1-variable.anchor_cd-variable.cds_synced)*gcd.max)+!buff.starlord.at_max_stacks*(0.5+buff.starlord.duration+gcd.max)+buff.starlord.at_max_stacks*(buff.eclipse.duration+gcd.max)
actions.kotg_st+=/solar_eclipse,if=fight_remains<buff.eclipse.duration+gcd.max+(((fight_remains-cooldown.ca_inc.remains<?0)<?(fight_remains-(cooldown.eclipse.full_recharge_time<?buff.eclipse.duration)<?0))>?((fight_remains-cooldown.ca_inc.remains<?0)>?buff.ca_inc.duration+gcd.max)+((fight_remains-(cooldown.eclipse.full_recharge_time<?buff.eclipse.duration)<?0)>?buff.eclipse.duration+gcd.max))
actions.kotg_st+=/fury_of_elune,if=cooldown.ca_inc.remains<(1+cooldown.force_of_nature.remains<gcd.max)*gcd.max&(buff.eclipse.remains<(1+cooldown.force_of_nature.remains<gcd.max)*gcd.max&fight_remains<buff.ca_inc.duration+(2+cooldown.force_of_nature.remains<gcd.max)*gcd.max+((fight_remains-cooldown.eclipse.remains<?0)>?buff.eclipse.duration+gcd.max)|fight_remains<buff.ca_inc.duration+(2+cooldown.force_of_nature.remains<gcd.max)*gcd.max)
actions.kotg_st+=/force_of_nature,if=cooldown.ca_inc.remains<gcd.max&(buff.eclipse.remains<gcd.max&fight_remains<buff.ca_inc.duration+gcd.max*2+((fight_remains-cooldown.eclipse.remains<?0)>?buff.eclipse.duration+gcd.max)|fight_remains<buff.ca_inc.duration+gcd.max*2)
actions.kotg_st+=/celestial_alignment,add_queue_lag=1,if=buff.eclipse.down&fight_remains<buff.ca_inc.duration+gcd.max+((fight_remains-cooldown.eclipse.remains<?0)>?buff.eclipse.duration+gcd.max)|fight_remains<buff.ca_inc.duration+gcd.max
actions.kotg_st+=/convoke_the_spirits,if=buff.harmony_of_the_grove.up&(astral_power<variable.starsurge_cost|(buff.touch_the_cosmos.react|buff.starweavers_warp.react|buff.starweavers_weft.react)&astral_power.deficit>60|buff.harmony_of_the_grove.remains<execute_time+gcd.max)&(fight_remains>cooldown.convoke_the_spirits.duration+execute_time|buff.ca_inc.up|fight_remains<cooldown.ca_inc.remains+execute_time+gcd.max)|(buff.ca_inc.up|buff.eclipse.up&fight_remains<cooldown.ca_inc.remains+execute_time+gcd.max)&fight_remains<cooldown.force_of_nature.remains+execute_time+gcd.max&(astral_power<variable.starsurge_cost|(buff.touch_the_cosmos.up|buff.starweavers_warp.up|buff.starweavers_weft.up)&astral_power.deficit>60|buff.eclipse.remains<execute_time+gcd.max)|fight_remains<execute_time+gcd.max
actions.kotg_st+=/starfall,if=buff.starweavers_warp.react
actions.kotg_st+=/starfall,if=(talent.starweaver&(talent.meteorites&(talent.incarnation_chosen_of_elune&talent.meteor_storm&!talent.power_of_goldrinn|buff.ca_inc.down&(talent.incarnation_chosen_of_elune|talent.stellar_amplification|!talent.power_of_goldrinn))|buff.eclipse.down&(talent.meteorites|talent.aetherial_kindling|talent.stellar_amplification&!talent.power_of_goldrinn))|buff.ca_inc.down&talent.meteorites&talent.aetherial_kindling&talent.stellar_amplification&!talent.power_of_goldrinn|buff.eclipse.down&talent.meteorites&(talent.aetherial_kindling|talent.stellar_amplification|!talent.power_of_goldrinn))&buff.touch_the_cosmos.react&!buff.starweavers_weft.react
actions.kotg_st+=/starsurge,if=buff.touch_the_cosmos.react|buff.starweavers_weft.react
actions.kotg_st+=/starsurge,if=buff.eclipse.up&(buff.touch_the_cosmos.react|buff.starweavers_weft.react|astral_power>=variable.starsurge_cost*(1+(buff.incarnation_chosen_of_elune.down&buff.ascendant_stars.down&buff.eclipse.remains<5))&(buff.ascendant_stars.up|variable.burst_hold_remains>5))
actions.kotg_st+=/starsurge,if=buff.eclipse.down&!buff.starlord.at_max_stacks&(variable.ecl_before_burst&!cooldown.eclipse.ready&variable.burst_hold_remains>30|!variable.ecl_before_burst&variable.burst_hold_remains>9-variable.cds_synced*3)&astral_power>=variable.starsurge_cost
actions.kotg_st+=/starsurge,if=astral_power.deficit<action.wrath.energize_amount+variable.passive_asp
actions.kotg_st+=/new_moon,if=astral_power.deficit>energize_amount
actions.kotg_st+=/half_moon,if=astral_power.deficit>energize_amount
actions.kotg_st+=/full_moon,if=astral_power.deficit>energize_amount
actions.kotg_st+=/wild_mushroom,if=buff.eclipse_solar.up&fight_remains<variable.burst_effective_cd+dot.fungal_growth.duration|fight_remains<dot.fungal_growth.duration+gcd.max
actions.kotg_st+=/wrath

actions.kotg_st_opener=moonfire,if=last_used<0
actions.kotg_st_opener+=/sunfire,if=last_used<0
actions.kotg_st_opener+=/potion
actions.kotg_st_opener+=/solar_eclipse,if=last_used<0
actions.kotg_st_opener+=/starfall,if=buff.starweavers_warp.react&(buff.ascendant_stars.up|astral_power<variable.burst_pooling_threshold)
actions.kotg_st_opener+=/starsurge,if=(buff.touch_the_cosmos.react|buff.starweavers_weft.react)&(buff.ascendant_stars.stack>!talent.natures_balance|astral_power<variable.burst_pooling_threshold)|buff.ascendant_stars.stack>!talent.natures_balance&astral_power>=variable.starsurge_cost
actions.kotg_st_opener+=/wrath,if=astral_power<variable.burst_pooling_threshold&action.wild_mushroom.last_used<0
actions.kotg_st_opener+=/sunfire,if=variable.burst_refresh_sunfire&variable.ca_burst_effective_cd=0
actions.kotg_st_opener+=/wild_mushroom
actions.kotg_st_opener+=/fury_of_elune
actions.kotg_st_opener+=/force_of_nature
actions.kotg_st_opener+=/use_items,check_existing=0
actions.kotg_st_opener+=/berserking
actions.kotg_st_opener+=/invoke_external_buff,name=power_infusion
actions.kotg_st_opener+=/celestial_alignment,add_queue_lag=1

# Global reset of gear stats to 0 so ONLY the profileset budget applies
gear_haste_rating=0
gear_mastery_rating=0
gear_crit_rating=0
gear_versatility_rating=0

# Items
head=enigmatic_dreamwatchers_somnolent_stare,id=271528,bonus_id=13692/13698/13750/13847/13848,gem_id=240983,enchant_id=8017,redirected_base_stats=271875
neck=aqirbane_reliquary,id=268265,bonus_id=40/13335/13668/13708/13848,gem_id=240918/240892,content_tuning=883
shoulders=enigmatic_dreamwatchers_plumage,id=271526,bonus_id=40/12854/13335/13694/13697,enchant_id=8001,content_tuning=807
back=silken_voodoo_drape,id=268253,bonus_id=13662/13848
chest=enigmatic_dreamwatchers_lunar_raiment,id=271531,bonus_id=12854/13690/13698,enchant_id=7987,redirected_base_stats=251159
wrists=enigmatic_dreamwatchers_wraps,id=271524,bonus_id=40/12854/13335/13696/13750,gem_id=240892,content_tuning=807
hands=enigmatic_dreamwatchers_gauntlets,id=271529,bonus_id=12854/13691/13697,redirected_base_stats=268234
waist=sash_of_the_forlorn_vessel,id=268256,bonus_id=13662/13750/13848,gem_id=240892
legs=enigmatic_dreamwatchers_leggings,id=271527,bonus_id=13693/13698/13848,enchant_id=7935,redirected_base_stats=268225
feet=arctic_explorers_legwraps,id=251153,bonus_id=12854/13662,enchant_id=7963
finger1=vile_alchemists_band,id=268249,bonus_id=40/12854/13335/13668,gem_id=240908,enchant_id=7967,content_tuning=883
finger2=loa_worshipers_band,id=251513,bonus_id=8960/12214/13751/13836/9627,gem_id=240898,enchant_id=7967
trinket1=vile_vial_of_volatile_venom,id=273796,bonus_id=40/12854/13440,content_tuning=883
trinket2=gebbos_bottomless_bag,id=270164,bonus_id=40/12854/13335,content_tuning=883
main_hand=janthrazet_the_soul_fang,id=271092,bonus_id=13662/13848,enchant_id=8041
off_hand=alnhara_lantern,id=245769,bonus_id=8960/12214/13751/13771/13836/9627,crafted_stats=32/49
"""

GLOBAL_SETTINGS = """
fight_style=Patchwerk
max_time=300
fixed_time=1
threads=0
iterations=10000
"""

def generate_4stat_grid(output_filename="moonkin_grid_4stat.simc", budget=3049, step=150):
    profiles = []
    count = 0

    for haste in range(0, budget + 1, step):
        for mastery in range(0, budget - haste + 1, step):
            for crit in range(0, budget - haste - mastery + 1, step):
                vers = budget - haste - mastery - crit

                profile_name = f"H{haste}_M{mastery}_C{crit}_V{vers}"

                p_code = f'profileset."{profile_name}"+=gear_haste_rating={haste}\n'
                p_code += f'profileset."{profile_name}"+=gear_mastery_rating={mastery}\n'
                p_code += f'profileset."{profile_name}"+=gear_crit_rating={crit}\n'
                p_code += f'profileset."{profile_name}"+=gear_versatility_rating={vers}\n'

                profiles.append(p_code)
                count += 1

    print(f"Generated {count} 4-stat profile variations for a budget of {budget} stats.")

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(GLOBAL_SETTINGS.strip() + "\n\n")
        f.write(FULL_PROFILE.strip() + "\n\n")
        f.write("# --- 4-STAT BUDGET MATRIX ---\n")
        f.write("".join(profiles))

if __name__ == "__main__":
    generate_4stat_grid()