import json
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler

# Model Load 
bz_smsm_dnn_model = tf.keras.models.load_model('/var/task/lambda-with-docker-container/model/dnn_bz_smsm_model')
sp_smdm_dnn_model = tf.keras.models.load_model('/var/task/lambda-with-docker-container/model/dnn_sp_smdm_model')

# Scaler Load
minmax_scaler = pickle.load(open('/var/task/lambda-with-docker-container/model/minmax_scaler.pkl','rb'))



def handler(event, context):

    body = event["body-json"]

    # event 로부터 feature 전처리
    lr = body["lr"]
    lc = body["lc"]
    rc = body["rc"]
    ld = body["ld"]
    rd = body["rd"]
    lnnz = body["lnnz"]
    rnnz = body["rnnz"]

    # 모델 입력으로 사용할 input_feature 생성
    input_feature = np.array([[lr,lc,rc,ld,rd,lnnz,rnnz]])

    # input_feature 에 minmax scaler 적용
    input_feature_scaler = minmax_scaler.transform(input_feature)

    # input_feature 에 대한 모델별 예측값 생성
    bz_smsm_dnn_result = bz_smsm_dnn_model.predict(input_feature_scaler)
    sp_smdm_dnn_result = sp_smdm_dnn_model.predict(input_feature_scaler)

    # sp_smdm 이 최적일 경우
    if (sp_smdm_dnn_result[0] <= bz_smsm_dnn_result[0]):
        optim_method = "sp_smdm"
    # bz_smsm 이 최적일 경우
    else:
        optim_method = "bz_smsm"
	# 결과 생성
    result = "bz_smsm : " + str(bz_smsm_dnn_result[0]) + " , " + \
		"sp_smdm : " + str(sp_smdm_dnn_result[0]) + " , " + \
		"optim_method : " + optim_method

	# 결과 반환
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }