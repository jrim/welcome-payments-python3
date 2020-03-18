# 웰컴 페이먼츠 PG사 클라이언트 

개인적으로 [웰컴페이먼츠](https://www.welcomepayments.co.kr/) 쓰려고 만든 모듈입니다.
Python 으로 PG 연동을 쉽게 만들어 주고 현재는 빌링결제만 되어 있습니다.
[아임포트 파이썬 모듈](https://github.com/iamport/iamport-rest-client-python/)을 참고하여 만들었습니다.
자세한 파라미터는 웰컴측 문서를 참고해주세요

사용법
=======

준비
------

사용하기 위해 객체를 만듭니다.

.. code-block:: python

    from welcome_payments import WelcomePayments

    wp = WelcomePayments(mid='{발급받은 MID}', sign_key='{발급받은 signKey}', mode='DEV')
    # mode ='DEV'(개발용), 'DEPLOY'(실제)


------

빌링 키 발급

.. code-block:: python

    response = wp.get_bill_key(**payload)

------

빌링 키로 결제

.. code-block:: python

    response = wp.bill_pay(**payload)

------

카드사 가져오기

.. code-block:: python

    response = wp.serch_card_prefix(**payload)

------

전체 취소

.. code-block:: python

    response = wp.cancle(**payload)