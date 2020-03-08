# Yahoo路線情報から駅名を経路付きで取得して返すAPI


Yahoo!路線情報(https://transit.yahoo.co.jp)
から乗車駅と降車駅を元に現在時刻での値段や経路をスクレイピングして，それを返す(Flask)

## 使用方法
乗車駅と降車駅の箇所を日本国内の駅に置き換える．そのままだと「降車駅」と「乗車駅」という駅は存在しないので失敗する．有名な観光地や建造物を入力しても結果の出力は成功する．Yahooの仕様．

現在時刻での値段
https://yahoo-train.herokuapp.com/price?from_station=乗車駅&to_station=降車駅

現在時刻での経路
https://yahoo-train.herokuapp.com/station?from_station=乗車駅&to_station=降車駅

